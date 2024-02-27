# OkCat

![](https://img.shields.io/badge/log-any%20format-orange.svg)
![](https://img.shields.io/badge/log-android-orange.svg)
![](https://img.shields.io/badge/log-ios-orange.svg)
![](https://img.shields.io/badge/log-backend-orange.svg)
![](https://img.shields.io/badge/license-Apache2-blue.svg)
[![](https://img.shields.io/badge/readme-English-blue.svg)](https://github.com/Jacksgong/okcat)
[![](https://img.shields.io/badge/readme-中文-blue.svg)](https://github.com/Jacksgong/okcat/blob/master/README-zh.md)
[![](https://img.shields.io/badge/pip-v1.3.0%20okcat-yellow.svg)](https://pypi.python.org/pypi/OkCat)
[![Build Status](https://travis-ci.org/Jacksgong/okcat.svg?branch=master)](https://travis-ci.org/Jacksgong/okcat)

An powerful log processor.

[中文文档](https://github.com/Jacksgong/okcat/blob/master/README-zh.md)

- The adb logcat handler is just update to JakeWharton's nice pidcat and I adapt it for more features.
- You can using this log processor with define you own `log-line-regex` and it can work for any log: iOS, Android, Backend, etc.  

## Features

> The most important feature is you can define any regex for any kind of log.

- highlight some keywords
![](https://github.com/Jacksgong/okcat/raw/master/arts/highlight-demo.png)
- trans msgs to some words
![](https://github.com/Jacksgong/okcat/raw/master/arts/trans-msg-demo.png)
- trans tags to some words
![](https://github.com/Jacksgong/okcat/raw/master/arts/trans-tag-demo.png)
- hide msg on logs
![](https://github.com/Jacksgong/okcat/raw/master/arts/hide-msg-demo.png)
- separate logs
![](https://github.com/Jacksgong/okcat/raw/master/arts/separate-demo.png)
- ignore msg on logs:
`when you provide such list, the msg start with provided msg will be ignored to printed`
- ignore tag on logs:
`when you provide such list, the tag in the list will be ignored to printed`

## How to Install

```shell
sudo pip install okcat
```

If you has not installed `pip` yet, you need to install it first:

1. `brew install python`
2. `sudo easy_install pip`

If you want to upgrade:

```shell
sudo pip install okcat --upgrade
```

## How to Use

---

#### Simplest test

1. Download: download [filedownloader.yml](https://github.com/Jacksgong/okcat/raw/master/demo-conf/filedownloader.yml) to the current folder or move to the `~/.okcat/` folder
2. Running: run the demo project on [Filedownloader](https://github.com/lingochamp/FileDownloader) repo to your Android phone and connect your Phone to computer
3. Execute: `okcat -y=filedownloader`
4. Done: now, you can checkout the colored logs on terminal, enjoy~

![](https://github.com/Jacksgong/okcat/raw/master/arts/demo.png)

---

#### 1. Define your config file(`.yml`)

You can create your own `.yaml` file as config file on `~/.okcat/` folder or the current folder you will execute `okcat` command, and the filename is free to choose, when you execute the okcat, we will ask you the configure file name you want to apply.

the following is demo of config file, Of course, you don't have to provide all configs such below, if you think which one is needed, just config that one.

```yml
# extends from exist yml file (provide only filename without `.yml` extension)
# from: exist-yml-name

# we will filter out logs with the provided package (name)
# this 'package' keyword is just using for android adb logcat
package: com.liulishuo.filedownloader.demo

# this 'log-line-regex' is just a regex for one line log
# now we support keyword: 'date' 'time' 'level' 'tag' 'process' 'thread' 'message'
# you don't have to provide all keyword, but you have to provide at least the 'message'
# such as: 'message="(\S*)"'
log-line-regex: 'date,time,process,thread,level,tag,message = "(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$"'

# on the case of filter logs from Android adb logcat, we using 'adb logcat -v brief -v threadtime' command to obtain logcat
# in the normal case you don't need ot provide this config, because there is a perfect one on the okcat internal
# but if you want to customize the regex log from adb logcat, it's free to define it such below
# adb-log-line-regex: 'date,time,process,thread,level,tag,message="(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$"'

# separator regex list
# you can provide multiple regex to separate serial logs
separator-regex-list:
  # on this case, if one line log match 'call start Url\[([^\]]*)\]' regex we will separate logs with \n and output a indie line with the '([^\]]*)' value as the title of separate
  - 'call start Url\[([^\]]*)\]'

# tag keyword list
# this list keyword is using for filter out which log need to be output
# all provided keyword will be using for compare with each line tag, if a line with tag not contain any keyword on 'tag-keyword-list' it will be ignore to output
tag-keyword-list:
  - 'FileDownloader'

# translate message map
# if a message on a line start with provide keyword on the 'trans-msg-map' we will add the value of the keyword on the start of the message, and the word of value will be colored to highlight it
trans-msg-map:
  # such as this case:
  # origin message: 'filedownloader:lifecycle:over xxx'
  # after translate: '| Task OVER | filedownloader:lifecycle:over xxx'
  'filedownloader:lifecycle:over': 'Task OVER'
  'fetch data with': 'Start Fetch'

# translate tag map
# if a tag on a line contain provide keyword on the 'trans-tag-map' we will add the value of the keyword on the start of the message, and the background of the value word will be colored to highlight it
trans-tag-map:
  # such as this case:
  # origin message: 'FileDownloader.DownloadTaskHunter  xxx'
  # after translate: 'FileDownloader.DownloadTaskHunter [Status Change] xxx'
  'DownloadTaskHunter': '[Status Change]'
  'ConnectTask': '[Request]'

# hide message list
# if a message on a line start with provide value on the 'hide-msg-list` and the length of the message is less than 100 word, it would be colored with gray to hide
hide-msg-list:
  # here we hide message start with 'notify progress' and '~~~callback' because it is too frequently to output and useless in most case
  - 'notify progress'
  - '~~~callback'

# highlight list
# if any value on the 'highlight-list' display on any message, the background of the value word would be colored to highlight it
highlight-list:
  - 'Path['
  - 'Url['
  - 'Tag['
  - 'range['

# ignore message list
# when you provide such list, the msg start with provided msg will be ignored to printed 
ignore-msg-list:
  - 'log start with this will be ignored' 

# ignore tag list
# when you provide such list, the tag in the list will be ignored to printed
ignore-tag-list:
  - 'tagToBeIgnored'
```

#### 2. Execute

You can just parse logcat from running adb:

```shell
okcat -y=your-conf-name
```

You also can parse your log file through:

```shell
okcat -y=your-conf-name your-log-path1 your-log-path2 your-log-path3 ... 
```

Simplest case for any developer:

```shell
okcat your.package.name
```

> Tips: You can use `command + k` on Terminal to flush all content on the session and start a new okcat parse instead of creating anthor new session.

## My Terminal Config

If you want to adapter the same theme like screenshot above, it's very easy:

- Firstly, please use [powerlevel9k](https://github.com/bhilburn/powerlevel9k) theme(Install the Powerlevel9k Theme and Powerline Fonts as the powerlevel9k repo readme doc said).
- Secondly, please config the [iTerm2-Neutron](https://github.com/Ch4s3/iTerm2-Neutron) color scheme.
- Thirdly, please config your shell(If you are using zsh, just add following code to the `~/.zshrc` file):
```
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time)
POWERLEVEL9K_TIME_FORMAT="%D{%H:%M:%S}"
POWERLEVEL9K_NODE_VERSION_BACKGROUND='022'
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
```

## Dev

Import to PyCharm, and Set the Project Structure:

![](https://github.com/Jacksgong/okcat/raw/master/arts/pycharm-build.jpg)

## LICENSE

```
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
```
