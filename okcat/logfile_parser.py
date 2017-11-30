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
from os.path import exists

from okcat.confloader import ConfLoader
from okcat.helper import get_conf_path
from okcat.logprocessor import LogProcessor
from okcat.terminalcolor import colorize, allocate_color

TIME_REGEX = r'\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d+'

class LogFileParser:
    filePaths = []
    valid = False
    processor = None
    hideSameTags = None
    logStreams = []
    cacheLines = []
    lineTimes = []

    def __init__(self, file_paths, hide_same_tags):
        self.filePaths = file_paths
        self.hideSameTags = hide_same_tags

    def setup(self, yml_file_name):
        for path in self.filePaths:
            if not exists(path):
                exit("log path: %s is not exist!" % path)
        self.processor = LogProcessor(self.hideSameTags)

        loader = ConfLoader()
        loader.load(get_conf_path(yml_file_name))

        self.processor.setup_trans(trans_msg_map=loader.get_trans_msg_map(),
                                   trans_tag_map=loader.get_trans_tag_map(),
                                   hide_msg_list=loader.get_hide_msg_list())
        self.processor.setup_separator(separator_rex_list=loader.get_separator_regex_list())
        self.processor.setup_highlight(highlight_list=loader.get_highlight_list())
        self.processor.setup_condition(tag_keywords=loader.get_tag_keyword_list())
        self.processor.setup_regex_parser(regex_exp=loader.get_log_line_regex())

    def color_line(self, line):
        msg_key, line_buf, match_precondition = self.processor.process(line)

        if not match_precondition:
            return

        if msg_key is not None:
            print('')
            print(u''.join(colorize(msg_key + ": ", fg=allocate_color(msg_key))).encode('utf-8').lstrip())

        print(u''.join(line_buf).encode('utf-8').lstrip())

    def popup_cache_line(self, popup_index):
        need_read_stream = self.logStreams[popup_index]
        new_line = need_read_stream.readline()
        if new_line:
            match_result = re.search(TIME_REGEX, new_line)
            if match_result:
                self.lineTimes.insert(popup_index, match_result.group())
                self.cacheLines.insert(popup_index, new_line)
            else:
                self.color_line(new_line)
                self.popup_cache_line(popup_index)
        else:
            need_read_stream.close()
            self.logStreams.pop(popup_index)



    def process(self):
        origin_index = 0
        for path in self.filePaths:
            stream = open(path, "r")
            self.logStreams.append(stream)
            self.popup_cache_line(origin_index)
            origin_index += 1

        while self.cacheLines:
            min_index = self.lineTimes.index(min(self.lineTimes))
            self.lineTimes.pop(min_index)
            selected_line = self.cacheLines.pop(min_index)
            self.color_line(selected_line)
            self.popup_cache_line(min_index)
            
