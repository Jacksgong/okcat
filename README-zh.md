# OkCat
强大的日志处理组件。

![](https://img.shields.io/badge/LogProcessor-OkCat-blue.svg)
[![](https://img.shields.io/badge/pip-okcat-green.svg)](https://pypi.python.org/pypi/OkCat)

[English Doc](https://github.com/Jacksgong/okcat)

ADB Logcat部分是基于JakeWharton的PID Cat，并且适配了各类OkCat的新特性。
你可以定义任意的日志正则表达式，来适配任意格式的日志，可以将其用于iOS、Android、后端等等。

##### 特性

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
pip install okcat
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

#### 1. 定义你的配置文件

你可以在`~/.okcat/`目录下创建你的yaml格式的配置文件，如果`~/.okcat`文件夹不存在先创建该文件夹；当然也可以直接在执行命令的当前目录创建yaml格式的配置文件。
文件名字可以是任何你想要的名字，在执行`okcat`的时候可以通过`-y=文件名`的形式，告知okcat想要应用的是哪个文件名的配置文件，okcat会默认在当前目录找，找不到会在`~/.okcat`目录下进行查找。

```yml
# 定义连线手机进行ADB处理时，需要过滤的包名；
# 如果不使用Android的ADB功能，便不需要配置
package: cn.dreamtobe.geekassistant

# 配置对于一行日志的正则表达式，目前支持正则出data、time、level、tag、process、thread、message
# 不过不一定要全部提供，至少需要提供一个message，如log-line-regex: 'message="(.\S*)"'
log-line-regex: 'data,time,level,tag,process,thread,message = "(.\S*) (.\S*) ([A-Z])/([^:[]*):\[(\d*):([^] ]*)\] (.*?)$"'

# 在Android的ADB的情况下，我们是使用adb logcat -v brief -v threadtime
# 一般情况下不需要adb-log-line-regex配置，我们已经有很完善的这块的正则，但是如果对这个需要特别定制便可以使用以下定制
# adb-log-line-regex: 'data,time,process,thread,level,tag,message="(.\S*) (.\S*) (\d*) (\d*) ([A-Z]) ([^:]*): (.*?)$"'

# 分割正则列表
# 可以提供多个正则表达式，对日志进行分割
separator-regex-list:
  # 对满足以下正则的那行日志开始进行分割，并且以(\d*)的内容作为分割的标题
  - 'MAIN,\d*,(\d*)'

# 标签关键字
# 如果不提供tag-keyword-list将会显示所有日志
# 如果如下提供了tag-keyword-list将会过滤日志，只显示tag中包含了这里列出关键字的日志
tag-keyword-list:
  - mylog

# 内容转译表
# 如果日志message中由表中key开头，将会使用彩色的文字在该message开头加上表中的value
trans-msg-map:
  # 如这个例子: 
  # 原message: 'connected-xxx xxx'
  # 转译后: '| SPDY已经连接 | connected-xxx xxx' 其中的'SPDY已经连接'会使用彩色的文字显示
  'connected-': 'SPDY已经连接'
  'disconnected-': 'SPDY已断开'

# 标签转译表
# 如果日志tag中包含表中key开头，将会使用彩色背景的文字在该message开头加上表中的value
trans-tag-map:
  # 如这个例子:
  # 原输出: 'AMyActivityLifecycleEvent	MainActivity onResumed'
  # 转译后: 'AMyActivityLifecycleEvent	[事件] MainActivity onResumed' 其中'[事件]'会使用彩色背景
  'MyActivityLifecycle': '[事件]'

# 隐藏消息列表
# 对以以下内容开头并且message长度小于100的内功进行灰色显示处理，在视觉上进行隐藏
hide-msg-list:
  # 这里案例因为心跳日志是非常频繁的日志，通常没有什么问题，因此将其着灰色
  - 'heart-beat'

# 高亮列表
# 对message中的以下内容，背景进行彩色处理使其高亮
highlight-list:
  - 'isSuccess='
```

## 2. 执行

> okcat的使用非常的简单。

如果你需要处理运行中App在Logcat的输出，只需要执行:

```shell
okcat -y=your-conf-name
```

如果你需要解析任意格式的日志，只需要执行:

```shell
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

