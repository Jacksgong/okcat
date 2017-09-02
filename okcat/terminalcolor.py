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

__author__ = 'jacks.gong'


class BashColors:
    def __init__(self):
        pass

    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(msg):
    print(BashColors.HEADER + msg + BashColors.END)


def print_exit(msg):
    print(BashColors.FAIL + msg + BashColors.END)


def print_error(msg):
    print(BashColors.FAIL + msg + BashColors.END)


def print_tips(msg):
    print(BashColors.UNDERLINE + msg + BashColors.END)


def print_warn(msg):
    print(BashColors.WARNING + msg + BashColors.END)


def print_key(msg):
    print(BashColors.GREEN + msg + BashColors.END)


def print_blue(msg):
    print(BashColors.BLUE + msg + BashColors.END)


def print_content_tips(msg):
    msg = BashColors.UNDERLINE + msg + BashColors.END
    print(msg)
    return msg + "\n"


def print_content_header(msg):
    msg = BashColors.HEADER + msg + BashColors.END
    print_content(msg)
    return msg + "\n"


def print_content(msg):
    print(msg)
    return msg


# -------------- color -----------------------------
RESET = '\033[0m'
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)


def termcolor(fg=None, bg=None):
    codes = []
    if fg is not None: codes.append('3%d' % fg)
    if bg is not None: codes.append('10%d' % bg)
    return '\033[%sm' % ';'.join(codes) if codes else ''


def colorize(message, fg=None, bg=None):
    if fg is None:
        if bg == BLACK:
            fg = WHITE
        else:
            fg = BLACK

    return termcolor(fg, bg) + message + RESET


TAGTYPES = {
    'V': colorize(' V ', fg=WHITE, bg=BLACK),
    'D': colorize(' D ', fg=BLACK, bg=BLUE),
    'I': colorize(' I ', fg=BLACK, bg=GREEN),
    'W': colorize(' W ', fg=BLACK, bg=YELLOW),
    'E': colorize(' E ', fg=BLACK, bg=RED),
    'F': colorize(' F ', fg=BLACK, bg=RED),
}

# for random color
KNOWN_TAGS = {
    'dalvikvm': WHITE,
    'Process': WHITE,
    'ActivityManager': WHITE,
    'ActivityThread': WHITE,
    'AndroidRuntime': CYAN,
    'jdwp': WHITE,
    'StrictMode': WHITE,
    'DEBUG': YELLOW,
}
LAST_USED = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]
LOG_FLOW_KEY_LAST_USED = [RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN]


def allocate_color(_key, loop_color=LAST_USED):
    if _key not in KNOWN_TAGS:
        KNOWN_TAGS[_key] = loop_color[0]

    _color = KNOWN_TAGS[_key]
    if _color in LAST_USED:
        loop_color.remove(_color)
        loop_color.append(_color)
    return _color
