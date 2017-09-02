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
from okcat.terminalcolor import colorize, allocate_color, BLACK

__author__ = 'JacksGong'


class Trans:
    trans_msg_map = None
    trans_tag_map = None
    hide_msg_list = None

    def __init__(self, trans_msg_map, trans_tag_map, hide_msg_list):
        self.trans_msg_map = trans_msg_map
        self.trans_tag_map = trans_tag_map
        self.hide_msg_list = hide_msg_list

    def trans_msg(self, msg):
        if self.trans_msg_map is None:
            return msg

        for key in self.trans_msg_map:
            if msg.startswith(key):
                value = self.trans_msg_map[key]
                return u'| %s | %s' % (colorize(value, fg=allocate_color(value)), msg)

        return msg

    def trans_tag(self, tag, msg):
        if self.trans_tag_map is None or tag is None:
            return msg

        for key in self.trans_tag_map:
            if key in tag:
                prefix = self.trans_tag_map[key]
                return u'%s %s' % (colorize(prefix, bg=allocate_color(prefix)), msg)

        return msg

    def hide_msg(self, msg):
        if self.hide_msg_list is None:
            return msg

        if msg.__len__() > 100:
            return msg

        for gray_msg in self.hide_msg_list:
            if msg.startswith(gray_msg):
                return colorize(msg, fg=BLACK)

        return msg
