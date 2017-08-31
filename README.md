# OkCat
An powerful log processor.

![](https://img.shields.io/badge/LogProcessor-OkCat-blue.svg)

The adb logcat handler is just update to JakeWharton's nice pidcat and I adapt it for more features.

You can using this log processor with define you own `log-line-regex` and it can work for any log: iOS, Android, Backend, etc.  

You can using powerful tool to do many things for logs:

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
# TODO
```

Now you can clone and execute `okcat.py` through `python okcat.py` temporary.

## How to Use

---

#### Simplest test

1. Create folder: `~/.okcat/`
2. Download: [filedownloader.yml](https://github.com/Jacksgong/okcat/raw/master/demo-conf/filedownloader.yml) and move to the `~/.okcat/` folder
3. Running: [Filedownloader-Demo](https://github.com/lingochamp/FileDownloader) on your Android phone 
4. Execute: `./okcat -y=filedownloader`
5. Checkout result on terminal

![](https://github.com/Jacksgong/okcat/raw/master/arts/demo.png)

---

#### 1. Define your config file( Option but recommended ):

You can create your own yaml file as config file one `~/.okcat/` or the current folder you will execute `okcat` command, and the filename is free to create, when you execute the okcat, we will ask you the configure file name you want to apply.

```yml
package: cn.dreamtobe.geekassistant
log-line-regex: 'data,time,level,tag,process,thread,message = "(.\S*) (.\S*) ([A-Z])/([^:[]*):\[(\d*):([^] ]*)\] (.*?)$"'

separator-regex-list:
	- 'MAIN,\d*,(\d*)

tag-keyword-list:
	- mylog

trans-msg-map:
	'connected-': "ConnectionMsg已经连接"
	'disconnected-': "ConnectionMsg已断开"

trans-tag-map:
	'MyActivityLifecycle': '[事件]'

hide-msg-list:
	- 'heart-beat'

highlight-list:
	- 'isSuccess='
```

## 2. Execute

You can just parse logcat from running adb:

```
./okcat -y=your_conf_name
```

You also can parse your log file through:

```
./okcat -y=your_conf_name your_log_path
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

