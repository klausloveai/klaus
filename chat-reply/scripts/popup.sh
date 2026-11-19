#!/bin/bash
# Chat 回复助手：弹一个 macOS 对话框，要 Klaus 手动点掉。
# 用法：popup.sh "<标题>" <<'EOF'
#       <正文，多行>
#       EOF
# 不阻塞调用方：对话框在后台进程里等点击。点「去看」打开 Chat 回复 session。
TITLE="${1:-Chat 回复助手}"
BODY="$(cat)"
SESSION_URL="claude://claude.ai/epitaxy/${CHAT_REPLY_SESSION:-local_b37fb074-a3d2-487d-8acb-15464f056ab7}"
LOG="$HOME/lingtu-cm-study/chat-reply/popup.log"
printf '%s  %s\n%s\n---\n' "$(date '+%F %T')" "$TITLE" "$BODY" >> "$LOG"

TMP="$(mktemp -t chatpopup)"
printf '%s' "$BODY" > "$TMP"
nohup /usr/bin/osascript - "$TITLE" "$TMP" "$SESSION_URL" >/dev/null 2>&1 <<'APPLESCRIPT' &
on run argv
  set t to item 1 of argv
  set b to read POSIX file (item 2 of argv) as «class utf8»
  set u to item 3 of argv
  set r to display alert t message b buttons {"知道了", "去看"} default button "知道了" cancel button "知道了"
  if button returned of r is "去看" then do shell script "open " & quoted form of u
end run
APPLESCRIPT
( sleep 5; rm -f "$TMP" ) >/dev/null 2>&1 &
