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

__author__ = 'JacksGong'


class LogSeparator:
    separator_rex_list = list()
    pre_separate_key = None

    def __init__(self, separator_rex_list):
        for regex_string in separator_rex_list:
            self.separator_rex_list.append(re.compile(r'%s' % regex_string))

    def process(self, msg):
        key = None
        for regex in self.separator_rex_list:
            matched_obj = regex.match(msg)
            if matched_obj is not None:
                key = matched_obj.groups()[0]
                break

        if self.pre_separate_key is None:
            if key is None:
                key = "unknown"
            self.pre_separate_key = key
            return key
        elif key is not None and self.pre_separate_key != key:
            return key
        else:
            return None
