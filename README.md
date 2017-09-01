# OkCat
An powerful log processor.

![](https://img.shields.io/badge/LogProcessor-OkCat-blue.svg)
[![](https://img.shields.io/badge/pip-okcat-green.svg)](https://pypi.python.org/pypi/OkCat)

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

## How to Install

```shell
sudo pip install okcat
```

If you has not installed `pip` yet, you need to install it first:

1. `brew install python`
2. `sudo easy_install pip`

## How to Use

---

#### Simplest test

1. Download: download [filedownloader.yml](https://github.com/Jacksgong/okcat/raw/master/demo-conf/filedownloader.yml) to the current folder or move to the `~/.okcat/` folder
2. Running: run the demo project on [Filedownloader](https://github.com/lingochamp/FileDownloader) repo to your Android phone and connect your Phone to computer
3. Execute: `okcat -y=filedownloader`
4. Done: now, you can checkout the colored logs on terminal, enjoy~

![](https://github.com/Jacksgong/okcat/raw/master/arts/demo.png)

---

#### 1. Define your config file(`.yaml`)

You can create your own yaml file as config file on `~/.okcat/` folder or the current folder you will execute `okcat` command, and the filename is free to choose, when you execute the okcat, we will ask you the configure file name you want to apply.

Of course, you don't have to provide each config, if you think which one is needed, just config that one.

```yml
package: cn.dreamtobe.geekassistant
log-line-regex: 'data,time,level,tag,process,thread,message = "(.\S*) (.\S*) ([A-Z])/([^:[]*):\[(\d*):([^] ]*)\] (.*?)$"'

separator-regex-list:
  - 'MAIN,\d*,(\d*)'

tag-keyword-list:
  - mylog

trans-msg-map:
  'connected-': 'Spdy Connected'
  'disconnected-': 'Spdy Disconnected'

trans-tag-map:
  'MyActivityLifecycle': '[Event]'

hide-msg-list:
  - 'heart-beat'

highlight-list:
  - 'isSuccess='
```

#### 2. Execute

You can just parse logcat from running adb:

```
okcat -y=your-conf-name
```

You also can parse your log file through:

```
okcat -y=your-conf-name your-log-path
```

## LICENSE

```
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
```

