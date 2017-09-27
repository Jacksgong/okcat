#!/usr/bin/python -u

"""
Copyright (C) 2017 Jacksgong(jacksgong.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from os.path import exists

from okcat.confloader import ConfLoader
from okcat.helper import LOG_LEVELS_MAP, get_conf_path, handle_home_case
from okcat.logprocessor import LogProcessor, indent_wrap
from okcat.logregex import LogRegex
from okcat.terminalcolor import termcolor, RED, RESET, YELLOW, GREEN, colorize, WHITE, allocate_color

__author__ = 'JacksGong'

# Script to highlight adb logcat output for console
# Originally written by Jeff Sharkey, http://jsharkey.org/
# Piping detection and popen() added by other Android team members
# Package filtering and output improvements by Jake Wharton, http://jakewharton.com
# Package adapt for okcat by Jacks Gong, https://jacksgong.com

import sys
import re
import subprocess
from subprocess import PIPE

# noinspection Annotator
PID_LINE = re.compile(r'^\w+\s+(\w+)\s+\w+\s+\w+\s+\w+\s+\w+\s+\w+\s+\w\s([\w|\.|\/]+)')
PID_START = re.compile(r'^.*: Start proc ([a-zA-Z0-9._:]+) for ([a-z]+ [^:]+): pid=(\d+) uid=(\d+) gids=(.*)$')
PID_START_5_1 = re.compile(r'^.*: Start proc (\d+):([a-zA-Z0-9._:]+)/[a-z0-9]+ for (.*)$')
PID_START_DALVIK = re.compile(
    r'^E/dalvikvm\(\s*(\d+)\): >>>>> ([a-zA-Z0-9._:]+) \[ userId:0 \| appId:(\d+) \]$')
PID_KILL = re.compile(r'^Killing (\d+):([a-zA-Z0-9._:]+)/[^:]+: (.*)$')
PID_LEAVE = re.compile(r'^No longer want ([a-zA-Z0-9._:]+) \(pid (\d+)\): .*$')
PID_DEATH = re.compile(r'^Process ([a-zA-Z0-9._:]+) \(pid (\d+)\) has died.?$')

ADB_LOG_REGEX_EXP = 'data,time,process,thread,level,tag,message="(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$"'

BUG_LINE = re.compile(r'.*nativeGetEnabledTags.*')
BACKTRACE_LINE = re.compile(r'^#(.*?)pc\s(.*?)$')
RULES = {
    # StrictMode policy violation; ~duration=319 ms: android.os.StrictMode$StrictModeDiskWriteViolation: policy=31 violation=1
    re.compile(r'^(StrictMode policy violation)(; ~duration=)(\d+ ms)')
    : r'%s\1%s\2%s\3%s' % (termcolor(RED), RESET, termcolor(YELLOW), RESET),
}


class Adb:
    all = None
    min_level = None
    package_name = None
    tag = None
    header_size = None
    ignored_tag = None

    log_regex = None
    catchall_package = None
    named_processes = None
    pids = None

    adb = None
    processor = None

    def __init__(self):
        pass

    def setup(self, args):
        self.processor = LogProcessor(args.hide_same_tags)

        self.min_level = LOG_LEVELS_MAP[args.min_level.upper()]
        self.all = args.all
        self.ignored_tag = args.ignored_tag
        self.tag = args.tag

        self.package_name = args.package_or_path
        self.processor.setup_condition(tag_keywords=args.tag_keywords)
        if args.yml is not None:
            conf_file_path = get_conf_path(args.yml)
            if not exists(handle_home_case(conf_file_path)):
                exit('you provide conf file path: ' + conf_file_path + ' is not exist!')

            conf_loader = ConfLoader()
            conf_loader.load(conf_file_path)

            yml_package = conf_loader.get_package()
            if yml_package is not None:
                self.package_name.append(yml_package)

            yml_adb_log_regex = conf_loader.get_adb_log_line_regex()
            if yml_adb_log_regex is not None:
                self.log_regex = LogRegex(yml_adb_log_regex)

            self.processor.setup_condition(tag_keywords=conf_loader.get_tag_keyword_list())
            self.processor.setup_trans(trans_msg_map=conf_loader.get_trans_msg_map(),
                                       trans_tag_map=conf_loader.get_trans_tag_map(),
                                       hide_msg_list=conf_loader.get_hide_msg_list())
            self.processor.setup_highlight(highlight_list=conf_loader.get_highlight_list())
            self.processor.setup_separator(separator_rex_list=conf_loader.get_separator_regex_list())

        if self.log_regex is None:
            self.log_regex = LogRegex(ADB_LOG_REGEX_EXP)

        base_adb_command = ['adb']
        if args.device_serial:
            base_adb_command.extend(['-s', args.device_serial])
        if args.use_device:
            base_adb_command.append('-d')
        if args.use_emulator:
            base_adb_command.append('-e')

        if args.current_app:
            system_dump_command = base_adb_command + ["shell", "dumpsys", "activity", "activities"]
            system_dump = subprocess.Popen(system_dump_command, stdout=PIPE, stderr=PIPE).communicate()[0]
            running_package_name = re.search(".*TaskRecord.*A[= ]([^ ^}]*)", system_dump).group(1)
            self.package_name.append(running_package_name)

        if len(self.package_name) == 0:
            self.all = True

        # Store the names of packages for which to match all processes.
        self.catchall_package = filter(lambda package: package.find(":") == -1, self.package_name)
        # Store the name of processes to match exactly.
        named_processes = filter(lambda package: package.find(":") != -1, self.package_name)
        # Convert default process names from <package>: (cli notation) to <package> (android notation) in the exact names match group.
        self.named_processes = map(lambda package: package if package.find(":") != len(package) - 1 else package[:-1],
                                   named_processes)

        self.header_size = args.tag_width + 1 + 3 + 1  # space, level, space

        # Only enable GC coloring if the user opted-in
        if args.color_gc:
            # GC_CONCURRENT freed 3617K, 29% free 20525K/28648K, paused 4ms+5ms, total 85ms
            key = re.compile(
                r'^(GC_(?:CONCURRENT|FOR_M?ALLOC|EXTERNAL_ALLOC|EXPLICIT) )(freed <?\d+.)(, \d+% free \d+./\d+., )(paused \d+ms(?:\+\d+ms)?)')
            val = r'\1%s\2%s\3%s\4%s' % (termcolor(GREEN), RESET, termcolor(YELLOW), RESET)

            RULES[key] = val

        adb_command = base_adb_command[:]
        adb_command.append('logcat')
        adb_command.extend(['-v', 'brief'])
        adb_command.extend(['-v', 'threadtime'])

        # Clear log before starting logcat
        if args.clear_logcat:
            adb_clear_command = list(adb_command)
            adb_clear_command.append('-c')
            adb_clear = subprocess.Popen(adb_clear_command)

            while adb_clear.poll() is None:
                pass

        if sys.stdin.isatty():
            self.adb = subprocess.Popen(adb_command, stdin=PIPE, stdout=PIPE)
        else:
            self.adb = FakeStdinProcess()
        self.pids = set()

        ps_command = base_adb_command + ['shell', 'ps']
        ps_pid = subprocess.Popen(ps_command, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        while True:
            try:
                line = ps_pid.stdout.readline().decode('utf-8', 'replace').strip()
            except KeyboardInterrupt:
                break
            if len(line) == 0:
                break

            pid_match = PID_LINE.match(line)
            if pid_match is not None:
                pid = pid_match.group(1)
                proc = pid_match.group(2)
                if proc in self.catchall_package:
                    self.pids.add(pid)

    def loop(self):
        app_pid = None

        while self.adb.poll() is None:
            # try:
            line = self.adb.stdout.readline().decode('utf-8', 'replace').strip()
            # except KeyboardInterrupt:
            #     break
            if len(line) == 0:
                break

            bug_line = BUG_LINE.match(line)
            if bug_line is not None:
                continue

            date, time, level, tag, owner, thread, message = self.log_regex.parse(line)
            if message is None:
                # print 'message is none with %s' % line
                continue

            tag = tag.strip()
            start = parse_start_proc(line)
            if start:
                line_package, target, line_pid, line_uid, line_gids = start
                if self.match_packages(line_package):
                    self.pids.add(line_pid)

                    app_pid = line_pid

                    linebuf = '\n'
                    linebuf += colorize(' ' * (self.header_size - 1), bg=WHITE)
                    linebuf += indent_wrap(' Process %s created for %s\n' % (line_package, target))
                    linebuf += colorize(' ' * (self.header_size - 1), bg=WHITE)
                    linebuf += ' PID: %s   UID: %s   GIDs: %s' % (line_pid, line_uid, line_gids)
                    linebuf += '\n'
                    print(linebuf)

            dead_pid, dead_pname = self.parse_death(tag, message)
            if dead_pid:
                self.pids.remove(dead_pid)
                linebuf = '\n'
                linebuf += colorize(' ' * (self.header_size - 1), bg=RED)
                linebuf += ' Process %s (PID: %s) ended' % (dead_pname, dead_pid)
                linebuf += '\n'
                print(linebuf)

            # Make sure the backtrace is printed after a native crash
            if tag == 'DEBUG':
                bt_line = BACKTRACE_LINE.match(message.lstrip())
                if bt_line is not None:
                    message = message.lstrip()
                    owner = app_pid

            # print '%s %s %s' % (owner, self.pids, tag)
            if not self.all and owner not in self.pids:
                continue
            if level in LOG_LEVELS_MAP and LOG_LEVELS_MAP[level] < self.min_level:
                continue
            if self.ignored_tag and tag_in_tags_regex(tag, self.ignored_tag):
                continue
            if self.tag and not tag_in_tags_regex(tag, self.tag):
                continue

            msg_key, linebuf, match_precondition = self.processor.process_decode_content(line, time, level, tag, owner,
                                                                                         thread,
                                                                                         message)
            if not match_precondition or linebuf is None:
                continue

            if msg_key is not None:
                print('')
                print(u''.join(colorize(msg_key + ": ", fg=allocate_color(msg_key))).encode('utf-8').lstrip())

            print(u''.join(linebuf).encode('utf-8').lstrip())

    def match_packages(self, token):
        if len(self.package_name) == 0:
            return True
        if token in self.named_processes:
            return True
        index = token.find(':')
        return (token in self.catchall_package) if index == -1 else (token[:index] in self.catchall_package)

    def parse_death(self, _tag, _message):
        if _tag != 'ActivityManager':
            return None, None
        kill = PID_KILL.match(_message)
        if kill:
            _pid = kill.group(1)
            package_line = kill.group(2)
            if self.match_packages(package_line) and _pid in self.pids:
                return _pid, package_line
        leave = PID_LEAVE.match(_message)
        if leave:
            _pid = leave.group(2)
            package_line = leave.group(1)
            if self.match_packages(package_line) and _pid in self.pids:
                return _pid, package_line
        death = PID_DEATH.match(_message)
        if death:
            _pid = death.group(2)
            package_line = death.group(1)
            if self.match_packages(package_line) and _pid in self.pids:
                return _pid, package_line
        return None, None  # This is a ducktype of the subprocess.Popen object


class FakeStdinProcess:
    def __init__(self):
        self.stdout = sys.stdin

    @staticmethod
    def poll():
        return None


def parse_start_proc(_line):
    _start = PID_START_5_1.match(_line)
    if _start is not None:
        _line_pid, _line_package, _target = _start.groups()
        return _line_package, _target, _line_pid, '', ''
    _start = PID_START.match(_line)
    if _start is not None:
        _line_package, _target, _line_pid, _line_uid, _line_gids = _start.groups()
        return _line_package, _target, _line_pid, _line_uid, _line_gids
    _start = PID_START_DALVIK.match(_line)
    if _start is not None:
        _line_pid, _line_package, _line_uid = _start.groups()
        return _line_package, '', _line_pid, _line_uid, ''
    return None


def tag_in_tags_regex(_tag, tags):
    return any(re.match(r'^' + t + r'$', _tag) for t in map(str.strip, tags))
