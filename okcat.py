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
from utils.adb import Adb

__author__ = 'JacksGong'
__version__ = '1.0.0'
__description__ = 'This python script used for combine several Android projects to one project.'

print("-------------------------------------------------------")
print("OkCat v" + __version__)
print("-------------------------------------------------------")

ID_DEBUG = True
file_path = None

if file_path is None:
    adb = Adb()
    adb.setup()
    while True:
        try:
            adb.loop()
        except KeyboardInterrupt:
            break
