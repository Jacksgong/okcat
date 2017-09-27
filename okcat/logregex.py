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

from okcat.terminalcolor import print_warn

__author__ = 'jacks.gong'

# val = 'data,time,process,thread,level,tag,message = "(.\S*) (.\S*) (\d*) (\d*) ([V|I|D|W|E]) ([^:]*): (.*)"'
REGEX_EXP_RE = re.compile(r"([^ =]*) *= *[\"|'](.*)[\"|']")
ALL_SUPPORT_KEY = ["data", "time", "process", "thread", "level", "tag", "message"]


class LogRegex:
    key_order = list()

    regex = None

    def __init__(self, regex_exp):
        keys, regex = REGEX_EXP_RE.match(regex_exp).groups()
        process_key_order = keys.split(',')

        self.regex = re.compile(r"%s" % regex)
        for key in process_key_order:
            key = key.strip()
            if key in ALL_SUPPORT_KEY:
                self.key_order.append(key)
            else:
                print_warn("not support key[%s] only support: %s" % (key, ALL_SUPPORT_KEY))

        print("find regex: " + self.key_order.__str__() + " with " + regex)

    def parse(self, line):
        data = None
        time = None
        process = None
        thread = None
        level = None
        tag = None
        message = None

        values = self.regex.match(line)

        if values is None:
            return data, time, level, tag, process, thread, message

        # print values.groups().__str__()
        i = 0
        for value in values.groups():
            key = self.key_order[i]
            i += 1
            if key == "data":
                data = value
            elif key == "time":
                time = value
            elif key == "process":
                process = value
            elif key == "thread":
                thread = value
            elif key == "level":
                level = value
            elif key == "tag":
                tag = value
            elif key == "message":
                message = value

        return data, time, level, tag, process, thread, message

    contain_data = None
    contain_time = None
    contain_thread = None
    contain_tag = None
    contain_level = None

    def is_contain_data(self):
        if self.contain_data is None:
            self.contain_data = self.is_contain_key("data")
        return self.contain_data

    def is_contain_time(self):
        if self.contain_time is None:
            self.contain_time = self.is_contain_key("time")
        return self.contain_time

    def is_contain_thread(self):
        if self.contain_thread is None:
            self.contain_thread = self.is_contain_key("thread")
        return self.contain_thread

    def is_contain_tag(self):
        if self.contain_tag is None:
            self.contain_tag = self.is_contain_key("tag")
        return self.contain_tag

    def is_contain_level(self):
        if self.contain_level is None:
            self.contain_level = self.is_contain_key("level")
        return self.contain_level

    def is_contain_key(self, key):
        return key in self.key_order
