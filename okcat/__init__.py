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
import argparse
from sys import argv

from okcat.adb import Adb
from okcat.helper import LOG_LEVELS, is_path
from okcat.logfile_parser import LogFileParser
from okcat.terminalcolor import print_tips, print_blue, print_warn, print_header, print_exit

__author__ = 'JacksGong'
__version__ = '1.4.0'
__description__ = 'This python script used for combine several Android projects to one project.'


def main():
    print("-------------------------------------------------------")
    print("                  OkCat v" + __version__)
    print("")
    print("Thanks for using okcat! Now, the doc is available on: ")
    print_blue("        https://github.com/Jacksgong/okcat")
    print("")
    print("                   Have Fun!")
    print("-------------------------------------------------------")

    parser = argparse.ArgumentParser(description='Filter logcat by package name')
    parser.add_argument('package_or_path', nargs='*',
                        help='This can be Application package name(s) or log file path(if the file from path is exist)')
    parser.add_argument('-y', '--yml_file_name', dest='yml', help='Using yml file you config on ~/.okcat folder')
    parser.add_argument('--hide-same-tags', dest='hide_same_tags', action='store_true',
                        help='Do not display the same tag name')

    # following args are just for parser
    # parser.add_argument('-k', '--keyword', dest='keyword', action='append', help='You can filter you care about log by this keyword(s)')

    # following args are just for adb
    parser.add_argument('-w', '--tag-width', metavar='N', dest='tag_width', type=int, default=23,
                        help='Width of log tag')
    parser.add_argument('-l', '--min-level', dest='min_level', type=str, choices=LOG_LEVELS + LOG_LEVELS.lower(),
                        default='V', help='Minimum level to be displayed')
    parser.add_argument('--color-gc', dest='color_gc', action='store_true', help='Color garbage collection')
    parser.add_argument('--current', dest='current_app', action='store_true',
                        help='Filter logcat by current running app')
    parser.add_argument('-s', '--serial', dest='device_serial', help='Device serial number (adb -s option)')
    parser.add_argument('-d', '--device', dest='use_device', action='store_true',
                        help='Use first device for log input (adb -d option)')
    parser.add_argument('-e', '--emulator', dest='use_emulator', action='store_true',
                        help='Use first emulator for log input (adb -e option)')
    parser.add_argument('-c', '--clear', dest='clear_logcat', action='store_true',
                        help='Clear the entire log before running')
    parser.add_argument('-t', '--tag', dest='tag', action='append', help='Filter output by specified tag(s)')
    parser.add_argument('-tk', '--tag_keywords', dest='tag_keywords', action='append',
                        help='Filter output by specified tag keyword(s)')
    parser.add_argument('-i', '--ignore-tag', dest='ignored_tag', action='append',
                        help='Filter output by ignoring specified tag(s)')
    parser.add_argument('-a', '--all', dest='all', action='store_true', default=False,
                        help='Print all log messages')

    # help
    if len(argv) == 2 and argv[1] == 'help':
        exit()

    args = parser.parse_args()

    file_paths = []
    candidate_path = args.package_or_path
    for path in candidate_path:
        if is_path(path):
            file_paths.append(path)

    if file_paths:
        if args.yml is None:
            print("")
            print_exit("Please using '-y=conf-name' to provide config file to parse this log file.")
            print("The config file is very very simple! More detail about config file please move to : https://github.com/Jacksgong/okcat")
            print("")
            print("-------------------------------------------------------")
            exit()

        parser = LogFileParser(file_paths, args.hide_same_tags)
        parser.setup(args.yml)
        parser.process()
    else:
        is_interrupt_by_user = False

        _adb = Adb()
        _adb.setup(args)
        try:
            _adb.loop()
        except KeyboardInterrupt:
            is_interrupt_by_user = True

        if not is_interrupt_by_user:
            print_warn('ADB CONNECTION IS LOST.')
