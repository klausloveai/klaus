#!/bin/zsh
# 个人微信：把关键词粘进左上搜索框并截图（不选中任何结果）。用法：wechat_search.sh "<关键词>" <输出.png>
# 关键词用粘贴不用键入：中文输入法会吞掉直接键入的英文字母。剪贴板用完还原。
OLD="$(pbpaste 2>/dev/null || true)"
front(){ osascript -e 'tell application "System Events" to get name of first process whose frontmost is true'; }
for i in 1 2 3; do open -a WeChat; sleep 0.8; [ "$(front)" = "WeChat" ] && break; done
[ "$(front)" = "WeChat" ] || { echo "WeChat 不在前台（现在是 $(front)），停止" >&2; exit 1; }
osascript -e 'tell application "System Events" to tell process "WeChat" to perform action "AXRaise" of window "WeChat"' >/dev/null 2>&1
B=$(osascript -e 'tell application "System Events" to tell process "WeChat" to get {position, size} of window "WeChat"' | tr -d ' ')
IFS=, read X Y WW HH <<< "$B"
~/.cache/wecom-skill/click $((X+163)) $((Y+32)); sleep 0.4      # 搜索框（窗口内左上）
printf '%s' "$1" | LC_ALL=en_US.UTF-8 pbcopy
[ "$(front)" = "WeChat" ] || { printf '%s' "$OLD" | pbcopy; echo "焦点丢了，停止" >&2; exit 1; }
osascript -e 'tell application "System Events" to keystroke "a" using command down'
osascript -e 'tell application "System Events" to keystroke "v" using command down'; sleep 1.5
printf '%s' "$OLD" | pbcopy
screencapture -x -R"$X,$Y,$WW,$HH" "$2"
