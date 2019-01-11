# 1.1.7

2019-01-11

- Fix: Fix wrong config field on the `log-line-regex` or `adb-log-line-regex` from 'data' to the correct one 'date'

# 1.1.6

2018-06-26

- Fix: fix encode issue on python3 - by [Ryfthink](https://github.com/Ryfthink)

# 1.1.5

2018-06-24

- Fix: some dvices adb lost connection, closes #9 - by [Ryfthink](https://github.com/Ryfthink)

# 1.1.4

2018-05-24

- Feat: support 'from' keyword to let yml config file extends from exist yml file

# 1.1.3

2017-12-01

- Feat: support combine and parse multiple log-files once time

# 1.1.2

2017-11-17

- Fix: fix unicode decode error on setup on windows system closes #4

# 1.1.1

2017-10-10

- Feat: show tips instead of crash when user don't provide config-file name to parse log file. Closes #2

# 1.1.0

2017-09-27

- Fix: fix import file failed on python 3.x

# 1.0.9

2017-09-16

- Fix: missing parentheses in call to 'print' error occurred on python 3.x Closes #1

# 1.0.8

2017-09-04

- Feat: handle the case of adb connection is lost when using adb logcat

# 1.0.7

2017-09-03

- Enhance: print each line when it has been parsed immediately rather than waiting for parsing whole file to handle case of large log file

# 1.0.6

2017-09-1

- Fix: cover the case of there is no 'level' keyword on `log-line-regex` case.
- Enhance: add `help` param on okcat, such as `okcat help`.
- Enhance: support `--hide-same-tags` param
- Fix: output all log when `log-line-regex` can't parse
- Fix: handle case of only message is valid
- Fix: fix print non-match content when the log can't match regex
- Fix: fix the default adb regex may wrong for some special case
