# 1.0.4

2017-09-1

- Fix: cover the case of there is no 'level' keyword on `log-line-regex` case.
- Enhance: add `help` param on okcat, such as `okcat help`.
- Enhance: support `--hide-same-tags` param
- Fix: output all log when `log-line-regex` can't parse
- Fix: handle case of only message is valid
- Fix: fix print non-match content when the log can't match regex
- Fix: fix the default adb regex may wrong for some special case
