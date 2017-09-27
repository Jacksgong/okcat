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
import re

from okcat.logregex import LogRegex
from okcat.logseparator import LogSeparator
from okcat.terminalcolor import allocate_color, colorize, TAGTYPES, termcolor, BLACK, RESET
from okcat.trans import Trans

__author__ = 'JacksGong'

TIME_WIDTH = 12
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


def keywords_regex(content, keywords):
    return any(re.match(r'.*' + t + r'.*', content) for t in map(str.strip, keywords))


class LogProcessor:
    hide_same_tags = None
    trans = None
    tag_keywords = None
    line_keywords = None
    separator = None
    regex_parser = None
    highlight_list = None
    # target_time = None

    # tmp
    last_msg_key = None
    last_tag = None
    pre_line_match = True

    def __init__(self, hide_same_tags):
        self.hide_same_tags = hide_same_tags

    def setup_trans(self, trans_msg_map, trans_tag_map, hide_msg_list):
        self.trans = Trans(trans_msg_map, trans_tag_map, hide_msg_list)

    def setup_separator(self, separator_rex_list):
        if separator_rex_list is not None:
            self.separator = LogSeparator(separator_rex_list)

    def setup_highlight(self, highlight_list):
        self.highlight_list = highlight_list

    def setup_condition(self, tag_keywords, line_keywords=None):
        self.tag_keywords = tag_keywords
        self.line_keywords = line_keywords

    def setup_regex_parser(self, regex_exp):
        self.regex_parser = LogRegex(regex_exp)

    def process(self, origin_line):
        origin_line = origin_line.decode('utf-8', 'replace').rstrip()

        if len(origin_line.strip()) <= 0:
            return None, None, False

        if self.regex_parser is None:
            return None, None, False

        date, time, level, tag, process, thread, message = self.regex_parser.parse(origin_line)
        if message is None:
            message = origin_line

        return self.process_decode_content(origin_line, time, level, tag, process, thread, message)

    # noinspection PyUnusedLocal
    def process_decode_content(self, line, time, level, tag, process, thread, message):

        match_condition = True

        # filter
        if self.tag_keywords is not None and tag is not None:
            if not keywords_regex(tag, self.tag_keywords):
                match_condition = False
                self.pre_line_match = False
            else:
                self.pre_line_match = True



        if self.line_keywords is not None:
            if not keywords_regex(line, self.line_keywords):
                match_condition = False
                self.pre_line_match = False
            else:
                self.pre_line_match = True

        if match_condition and tag is None and not self.pre_line_match:
            match_condition = False

        # if 'special world' in line:
        #     match_precondition = True

        if not match_condition:
            return None, None, None

        msgkey = None
        # the handled current line
        linebuf = ''

        # time
        if time is not None:
            time = time[-TIME_WIDTH:].rjust(TIME_WIDTH)
            linebuf += time
            linebuf += ' '
        elif self.regex_parser.is_contain_time():
            linebuf += ' ' * TIME_WIDTH
            linebuf += ' '

        # thread
        if thread is not None:
            thread = thread.strip()
            thread = thread[-THREAD_WIDTH:].rjust(THREAD_WIDTH)
            linebuf += thread
            linebuf += ' '
        elif self.regex_parser.is_contain_thread():
            linebuf += ' ' * THREAD_WIDTH
            linebuf += ' '

        # tag
        if tag is not None and (not self.hide_same_tags or tag != self.last_tag):
            self.last_tag = tag
            tag = tag.strip()
            color = allocate_color(tag)
            tag = tag.strip()
            tag = tag[-TAG_WIDTH:].rjust(TAG_WIDTH)
            linebuf += colorize(tag, fg=color)
            linebuf += ' '
        elif self.regex_parser.is_contain_tag():
            linebuf += ' ' * TAG_WIDTH
            linebuf += ' '

        # level
        if level is not None:
            if level in TAGTYPES:
                linebuf += TAGTYPES[level]
            else:
                linebuf += ' ' + level + ' '
            linebuf += ' '
        elif self.regex_parser.is_contain_level():
            linebuf += ' '
            linebuf += ' '

        # message
        # -separator
        if self.separator is not None:
            msgkey = self.separator.process(message)

        # -trans
        if self.trans is not None:
            message = self.trans.trans_msg(message)
            message = self.trans.hide_msg(message)
            message = self.trans.trans_tag(tag, message)

        if self.highlight_list is not None:
            for highlight in self.highlight_list:
                if highlight in message:
                    message = message.replace(highlight,
                                              termcolor(fg=BLACK, bg=allocate_color(highlight)) + highlight + RESET)

        linebuf += message

        return msgkey, linebuf, match_condition
