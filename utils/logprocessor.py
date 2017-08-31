#!/usr/bin/python -u

"""
Copyright (C) 2017 Jacksgong(blog.dreamtobe.cn)

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

from utils.logregex import LogRegex
from utils.logseparator import LogSeparator
from utils.terminalcolor import allocate_color, colorize, TAGTYPES
from utils.trans import Trans

__author__ = 'JacksGong'

THREAD_WIDTH = 12
TAG_WIDTH = 23

width = -1
# noinspection PyBroadException
try:
    # Get the current terminal width
    import fcntl, termios, struct

    h, width = struct.unpack('hh', fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('hh', 0, 0)))
except:
    pass

header_size = TAG_WIDTH + 1 + 3 + 1  # space, level, space


def indent_wrap(message):
    return message


class LogProcessor:
    # output
    warningLine = 0
    warningLogs = ""
    errorLine = 0
    errorLogs = ""

    trans = None
    separator = None
    log_regex = None
    regex_parser = None
    message_wildcard_list = None
    # target_time = None
    keywords = None

    # tmp
    last_tag = None
    last_msg_key = None

    def __init__(self, message_wildcard_list=None, keywords=None, regex_exp=None):

        self.message_wildcard_list = message_wildcard_list
        self.keywords = keywords

        if regex_exp is not None:
            self.log_regex = LogRegex(regex_exp)

    def setup_trans(self, trans_msg_map, trans_tag_map, hide_msg_list):
        self.trans = Trans(trans_msg_map, trans_tag_map, hide_msg_list)

    def setup_separator(self, separator_rex_list):
        self.separator = LogSeparator(separator_rex_list)

    def process(self, origin_line):
        origin_line = origin_line.decode('utf-8', 'replace').strip()

        if self.regex_parser is None:
            return None, None, False

        date, time, level, tag, process, thread, message = self.log_regex.parse(origin_line)
        if message is None:
            return None, None, False

        return self.process_decode_content(origin_line, time, level, tag, process, thread, message)

    def process_decode_content(self, line, time, level, tag, process, thread, message):

        match_precondition = False
        message_wildcard_list = self.message_wildcard_list

        if message_wildcard_list is None:
            match_precondition = True
        else:
            for message_wildcard in self.message_wildcard_list:
                if message_wildcard in line:
                    match_precondition = True
                    break

        msgkey = None
        # the handled current line
        linebuf = ''

        # if 'special world' in line:
        #     match_precondition = True

        if match_precondition:

            # time
            linebuf += time + ' '

            # thread
            thread = thread.strip()
            thread = thread[-THREAD_WIDTH:].rjust(THREAD_WIDTH)
            linebuf += thread
            linebuf += ' '

            # tag
            tag = tag.strip()
            if tag != self.last_tag:
                self.last_tag = tag
                color = allocate_color(tag)
                tag = tag.strip()
                tag = tag[-TAG_WIDTH:].rjust(TAG_WIDTH)
                linebuf += colorize(tag, fg=color)
            else:
                linebuf += ' ' * TAG_WIDTH
            linebuf += ' '

            # level
            if level in TAGTYPES:
                linebuf += TAGTYPES[level]
            else:
                linebuf += ' ' + level + ' '
            linebuf += ' '

            # message
            # -trans
            if self.trans is not None:
                message = self.trans.trans_msg(message)
                message = self.trans.hide_msg(message)
                message = self.trans.trans_tag(tag, message)

            # -separator
            if self.separator is not None:
                msgkey = self.separator.process(message)

            linebuf += message

            if 'W' in level:
                self.warningLine += 1
                self.warningLogs += linebuf + '\n'
            elif 'E' in level:
                self.errorLine += 1
                self.errorLogs += linebuf + '\n'

        return msgkey, linebuf, match_precondition
