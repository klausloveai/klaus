#!/bin/bash
# Chat 回复助手：右上角系统通知（alerter），不挡屏幕，点掉才消失。
# 用法：popup.sh "<标题>" "<副标题>" <<'EOF'
#       <正文：通知里只显示前几行，写最要紧的>
#       EOF
# 按钮：「知道了」关掉；「去看」打开 Chat 回复 session。完整内容同时追加进 popup.log。
TITLE="${1:-Chat 回复助手}"
SUB="${2:-}"
BODY="$(cat)"
SESSION_URL="claude://claude.ai/epitaxy/${CHAT_REPLY_SESSION:-local_b37fb074-a3d2-487d-8acb-15464f056ab7}"
LOG="$HOME/lingtu-cm-study/chat-reply/popup.log"
printf '%s  %s | %s\n%s\n---\n' "$(date '+%F %T')" "$TITLE" "$SUB" "$BODY" >> "$LOG"

# alerter 会一直等到点击才返回，所以放后台；点「去看」或点通知本身就打开 session。
nohup bash -c '
  r=$(/opt/homebrew/bin/alerter --title "$1" --subtitle "$2" --message "$3" \
        --actions "去看" --close-label "知道了" --sound default --group "chat-reply-$$" 2>/dev/null)
  case "$r" in "去看"|"@CONTENTCLICKED"|"@ACTIONCLICKED") open "$4" ;; esac
' _ "$TITLE" "$SUB" "$BODY" "$SESSION_URL" >/dev/null 2>&1 &
