# OkCat

![](https://img.shields.io/badge/log-any%20format-orange.svg)
![](https://img.shields.io/badge/log-android-orange.svg)
![](https://img.shields.io/badge/log-ios-orange.svg)
![](https://img.shields.io/badge/log-backend-orange.svg)
![](https://img.shields.io/badge/license-Apache2-blue.svg)
[![](https://img.shields.io/badge/readme-English-blue.svg)](https://github.com/Jacksgong/okcat)
[![](https://img.shields.io/badge/readme-中文-blue.svg)](https://github.com/Jacksgong/okcat/blob/master/README-zh.md)
[![](https://img.shields.io/badge/pip-v1.1.7%20okcat-yellow.svg)](https://pypi.python.org/pypi/OkCat)
[![Build Status](https://travis-ci.org/Jacksgong/okcat.svg?branch=master)](https://travis-ci.org/Jacksgong/okcat)

强大的日志处理组件。

[English Doc](https://github.com/Jacksgong/okcat)

- 你可以定义任意的日志正则表达式，来适配任意格式的日志，可以将其用于iOS、Android、后端等等。
- ADB Logcat部分是基于JakeWharton的PID Cat，并且适配了各类OkCat的新特性 。

Andrdoid工程师查看ADB Logcat最简单的使用:

```shell
okcat 包名
```

## 特性

> 最主要的特性是：你可以为不同的日志定义自己的正则表达式，以此适配各种类型的日志处理。

- 高亮一些关键字
![](https://github.com/Jacksgong/okcat/raw/master/arts/highlight-demo.png)
- 转译日志内容
![](https://github.com/Jacksgong/okcat/raw/master/arts/trans-msg-demo.png)
- 转译Tag
![](https://github.com/Jacksgong/okcat/raw/master/arts/trans-tag-demo.png)
- 隐藏一些日志
![](https://github.com/Jacksgong/okcat/raw/master/arts/hide-msg-demo.png)
- 对连续的日志进行分割
![](https://github.com/Jacksgong/okcat/raw/master/arts/separate-demo.png)

## 如何安装

```shell
sudo pip install okcat
```

如果你还没有安装`pip`，你需要先安装`pip`:

1. `brew install python`
2. `sudo easy_install pip`

如果你想要升级:

```
sudo pip install okcat --upgrade
```

## 如何使用

---

#### 最简单的测试

1. 下载[filedownloader.yml](https://github.com/Jacksgong/okcat/raw/master/demo-conf/filedownloader.yml)在当前目录，或者移动到`~/.okcat/`目录中
3. 运行这个[Filedownloader-Demo](https://github.com/lingochamp/FileDownloader)项目中的demo项目，并运行到你的Android手机上，然后将手机连接电脑
4. 执行: `okcat -y=filedownloader`
5. 此时日志就会根据[filedownloader.yml](https://github.com/Jacksgong/okcat/raw/master/demo-conf/filedownloader.yml)的配置输出了

![](https://github.com/Jacksgong/okcat/raw/master/arts/demo.png)

---

#### 1. 定义你的配置文件(`.yml`)

你可以在`~/.okcat/`目录下创建你的yaml格式的配置文件，如果`~/.okcat`文件夹不存在先创建该文件夹；当然也可以直接在执行命令的当前目录创建yaml格式的配置文件。
文件名字可以是任何你想要的名字，在执行`okcat`的时候可以通过`-y=文件名`的形式，告知okcat想要应用的是哪个文件名的配置文件，okcat会默认在当前目录找，找不到会在`~/.okcat`目录下进行查找。

下面是配置文件的案例，里面列出了目前支持的所有的配置，当然你不需要配置所有的特性，只需要配置你需要的即可。

```yml
# 继承存在的其他yml的配置(不需要`.yml`后缀)
from: exist-yml-file-name

# 定义连线手机进行ADB处理时，需要过滤的包名；
# 如果不使用Android的ADB功能，便不需要配置
package: com.liulishuo.filedownloader.demo

# 配置对于一行日志的正则表达式，目前支持正则出date、time、level、tag、process、thread、message
# 不过不一定要全部提供，至少需要提供一个message
# 如log-line-regex: 'message="(.\S*)"'
log-line-regex: 'date,time,process,thread,level,tag,message = "(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$"'

# 在Android的ADB的情况下，我们是使用adb logcat -v brief -v threadtime
# 一般情况下不需要adb-log-line-regex配置，我们已经有很完善的这块的正则，但是如果对这个需要特别定制便可以使用以下定制
# adb-log-line-regex: 'date,time,process,thread,level,tag,message="(.\S*) *(.\S*) *(\d*) *(\d*) *([A-Z]) *([^:]*): *(.*?)$"'

# 分割正则列表
# 可以提供多个正则表达式，对日志进行分割
separator-regex-list:
  # 对满足以下正则的那行日志开始进行分割，并且以([^\]]*)的内容作为分割的标题
  - 'call start Url\[([^\]]*)\]'

# 标签关键字
# 如果不提供tag-keyword-list将会显示所有日志
# 如果如下提供了tag-keyword-list将会过滤日志，只显示tag中包含了这里列出关键字的日志
tag-keyword-list:
  - 'FileDownloader'

# 内容转译表
# 如果日志message中由表中key开头，将会使用彩色的文字在该message开头加上表中的value
trans-msg-map:
  # 如这个例子:
  # 原message: 'filedownloader:lifecycle:over xxx'
  # 转译后: '| 任务结束 | filedownloader:lifecycle:over xxx' 其中的'任务结束'会使用彩色的文字显示
  'filedownloader:lifecycle:over': '任务结束'
  'fetch date with': '开始拉取'

# 标签转译表
# 如果日志tag中包含表中key开头，将会使用彩色背景的文字在该message开头加上表中的value
trans-tag-map:
  # 如这个例子:
  # 原输出: 'FileDownloader.DownloadTaskHunter  xxx'
  # 转译后: 'FileDownloader.DownloadTaskHunter [状态切换] xxx' 其中'[状态切换]'会使用彩色背景
  'DownloadTaskHunter': '[状态切换]'
  'ConnectTask': '[请求]'

# 隐藏消息列表
# 对以以下内容开头并且message长度小于100的内功进行灰色显示处理，在视觉上进行隐藏
hide-msg-list:
  # 这里案例因为心跳日志是非常频繁的日志，通常没有什么问题，因此将其着灰色
  - 'notify progress'
  - '~~~callback'

# 高亮列表
# 对message中的以下内容，背景进行彩色处理使其高亮
highlight-list:
  - 'Path['
  - 'Url['
  - 'Tag['
  - 'range['
```

#### 2. 执行

> okcat的使用非常的简单。

如果你需要处理运行中App在Logcat的输出，只需要执行:

```shell
okcat -y=your-conf-name
```

如果你需要解析任意格式的日志，只需要执行:

```shell
okcat -y=your-conf-name your-log-path1 your-log-path2 your-log-path3 ... 
```

> 小技巧: 你在终端中使用`Command + K`来刷新当前回话中的所有内容，以此快速启动新的okcat解析，而不用再另外创建一个新的会话。

## 我的终端的风格配置

如果你想要适配和上面截图一样的终端风格，非常简单:

- 首先，请使用[powerlevel9k](https://github.com/bhilburn/powerlevel9k)主题(正如Powerlevel9k文档提到的安装Powerlevel9k主题，并且安装Powerline字体).
- 其次，请配置[iTerm2-Neutron](https://github.com/Ch4s3/iTerm2-Neutron)色系.
- 最后, 请配置ini的shell(如果你使用的是zsh，只需要添加下列代码到`~/.zshrc`文件中):
```
POWERLEVEL9K_LEFT_PROMPT_ELEMENTS=(dir vcs)
POWERLEVEL9K_RIGHT_PROMPT_ELEMENTS=(status time)
POWERLEVEL9K_TIME_FORMAT="%D{%H:%M:%S}"
POWERLEVEL9K_NODE_VERSION_BACKGROUND='022'
POWERLEVEL9K_SHORTEN_DIR_LENGTH=2
```

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
