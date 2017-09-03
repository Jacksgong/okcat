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

from helper import get_conf_path
from logprocessor import LogProcessor
from terminalcolor import colorize, allocate_color

from okcat.confloader import ConfLoader


class LogFileParser:
    file_path = None
    valid = False
    processor = None
    hide_same_tags = None

    def __init__(self, file_path, hide_same_tags):
        self.file_path = file_path
        self.hide_same_tags = hide_same_tags

    def setup(self, yml_file_name):
        if not exists(self.file_path):
            exit("log path: %s is not exist!" % self.file_path)
        self.processor = LogProcessor(self.hide_same_tags)

        loader = ConfLoader()
        loader.load(get_conf_path(yml_file_name))

        self.processor.setup_trans(trans_msg_map=loader.get_trans_msg_map(),
                                   trans_tag_map=loader.get_trans_tag_map(),
                                   hide_msg_list=loader.get_hide_msg_list())
        self.processor.setup_separator(separator_rex_list=loader.get_separator_regex_list())
        self.processor.setup_highlight(highlight_list=loader.get_highlight_list())
        self.processor.setup_condition(tag_keywords=loader.get_tag_keyword_list())
        self.processor.setup_regex_parser(regex_exp=loader.get_log_line_regex())

    def process(self):
        log_file = open(self.file_path, 'r')

        for line in log_file:
            msg_key, linebuf, match_precondition = self.processor.process(line)

            if not match_precondition:
                continue

            if msg_key is not None:
                print ''
                print u''.join(colorize(msg_key + ": ", fg=allocate_color(msg_key))).encode('utf-8').lstrip()

            print u''.join(linebuf).encode('utf-8').lstrip()
