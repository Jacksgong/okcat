#!/usr/bin/env python
# coding: utf-8

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

import yaml

from okcat.helper import handle_home_case

__author__ = 'JacksGong'


class ConfLoader:
    yml_conf = None

    def __init__(self):
        pass

    def load(self, yml_file_path):
        with open(handle_home_case(yml_file_path), 'r') as stream:
            try:
                self.yml_conf = yaml.load(stream)
                # print(u'find yml configuration on %s:' % yml_file_path)
                # self.dump()

            except yaml.YAMLError as exc:
                print(exc)

    def get_package(self):
        return self.get_value('package')

    def get_tag_keyword_list(self):
        return self.get_value('tag-keyword-list')

    def get_trans_msg_map(self):
        return self.get_value('trans-msg-map')

    def get_trans_tag_map(self):
        return self.get_value('trans-tag-map')

    def get_hide_msg_list(self):
        return self.get_value('hide-msg-list')

    def get_highlight_list(self):
        return self.get_value('highlight-list')

    def get_log_line_regex(self):
        return self.get_value('log-line-regex')

    def get_adb_log_line_regex(self):
        return self.get_value('adb-log-line-regex')

    def get_separator_regex_list(self):
        return self.get_value('separator-regex-list')

    def get_value(self, keyword):
        if keyword not in self.yml_conf:
            return None
        return self.yml_conf[keyword]

    def dump(self):
        print('package: %s' % self.get_package())
        print('log-line-regex: %s' % self.get_log_line_regex())
        print('adb-log-line-regex: %s' % self.get_adb_log_line_regex())
        self.dump_list('tag-keyword-list')
        self.dump_unicode_map('trans-msg-map')
        self.dump_unicode_map('trans-tag-map')
        self.dump_list('hide-msg-list')
        self.dump_list('highlight-list')
        self.dump_list('separator-regex-list')

    def dump_unicode_map(self, map_key):
        unicode_map = self.get_value(map_key)
        if unicode_map is None:
            print('%s: None' % map_key)
        else:
            print('%s:' % map_key)
            for key in unicode_map:
                print(u'    "%s" : "%s"' % (key, unicode_map[key]))

    def dump_list(self, list_key):
        cur_list = self.get_value(list_key)
        if cur_list is None:
            print('%s: None' % list_key)
        else:
            print('%s: ' % list_key)
            for value in cur_list:
                print('    - %s' % value)
