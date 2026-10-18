#!/bin/zsh
# 企业微信「发起群聊」选人框：把关键词粘进框内搜索并截图（不勾选）。用法：wecom_picker_search.sh "<名字>" <输出.png>
# 坐标按企微窗口位置现算：选人框搜索栏 ≈ 窗口左上 +(431,142)pt。窗口挪过要先截图核对。
OLD="$(pbpaste 2>/dev/null || true)"
front(){ osascript -e 'tell application "System Events" to get name of first process whose frontmost is true'; }
osascript -e 'tell application "企业微信" to activate'; sleep 0.5
[ "$(front)" = "企业微信" ] || { echo "企业微信不在前台，停止" >&2; exit 1; }
B=$(osascript -e 'tell application "System Events" to tell process "企业微信" to get {position, size} of window "企业微信"' | tr -d ' ')
IFS=, read X Y WW HH <<< "$B"
~/.cache/wecom-skill/click $((X+431)) $((Y+142)); sleep 0.3
printf '%s' "$1" | LC_ALL=en_US.UTF-8 pbcopy
[ "$(front)" = "企业微信" ] || { printf '%s' "$OLD" | pbcopy; echo "焦点丢了，停止" >&2; exit 1; }
osascript -e 'tell application "System Events" to keystroke "a" using command down'
osascript -e 'tell application "System Events" to keystroke "v" using command down'; sleep 1.3
printf '%s' "$OLD" | pbcopy
screencapture -x -R"$X,$Y,$WW,$HH" "$2"
