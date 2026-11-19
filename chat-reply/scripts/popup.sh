#!/bin/bash
# Chat 回复助手：右上角弹系统通知（不挡屏幕）。
# 要它一直挂着、点掉才消失：系统设置 → 通知 → 「脚本编辑器 / Script Editor」→ 提醒样式选「持续 / Persistent」（只需设一次）。
# 用法：popup.sh "<标题>" "<副标题>" <<'EOF'
#       <正文：通知里只显示前几行，写最要紧的>
#       EOF
# 完整内容同时追加进 popup.log。
TITLE="${1:-Chat 回复助手}"
SUB="${2:-}"
BODY="$(cat)"
LOG="$HOME/lingtu-cm-study/chat-reply/popup.log"
printf '%s  %s | %s\n%s\n---\n' "$(date '+%F %T')" "$TITLE" "$SUB" "$BODY" >> "$LOG"

/usr/bin/osascript - "$TITLE" "$SUB" "$BODY" <<'APPLESCRIPT'
on run argv
  display notification (item 3 of argv) with title (item 1 of argv) subtitle (item 2 of argv)
end run
APPLESCRIPT
