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
