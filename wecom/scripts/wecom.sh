#!/bin/zsh
# 操作企业微信 Mac 客户端：找群、读聊天记录、放草稿、找本地文件。
# 所有命令都通过模拟键盘和截图完成，不碰企微的加密数据库。
#
#   wecom.sh setup                 检查权限和工具，编译滚轮小工具
#   wecom.sh bounds                打印企微主窗口位置和默认聊天区域
#   wecom.sh search "<群名>"       把群名填进搜索框，停在搜索结果（不打开）
#   wecom.sh open [序号]           打开第 N 条搜索结果（默认第 1 条）
#   wecom.sh shot <输出.png> [区域] 截当前聊天区域
#   wecom.sh capture <输出目录> [区域] [步长]  从底部往上滚到顶，逐屏截图并拼成 strip_XX.png（时间从早到晚）
#   wecom.sh paste <草稿文件>      把文字贴进当前会话输入框（不发送）
#   wecom.sh paste-image <图片>    把图片贴进当前会话输入框（不发送）
#   wecom.sh read-input            读出当前输入框里的文字
#   wecom.sh send                  按回车发送。只有用户明确说「发送」才能用
#   wecom.sh files "<文件名关键词>" 在本机企微缓存里找下载过的文件
#
# 区域格式：x,y,宽,高（单位 point），省略时按窗口位置自动算，第一次用要截图核对。

set -euo pipefail
export LC_ALL=en_US.UTF-8   # 否则 pbcopy 按 MacRoman 处理，中文变乱码
HERE="${0:A:h}"
SCROLL="$HOME/.cache/wecom-skill/scroll"   # 编译到用户目录，技能目录可能只读或被更新覆盖

front_app() { osascript -e 'tell application "System Events" to get name of first process whose frontmost is true'; }

# System Events 的 set frontmost / AXRaise 在有的机器上不生效（按键会打到别的程序），
# 所以改用 activate，并确认企微真的到了最前面才继续。
raise_main() {
  local i
  for i in 1 2 3 4 5; do
    osascript -e 'tell application "企业微信" to activate' >/dev/null
    sleep 0.6
    if [[ "$(front_app)" == "企业微信" ]]; then
      osascript -e 'tell application "System Events" to tell process "企业微信" to perform action "AXRaise" of window "企业微信"' >/dev/null 2>&1 || true
      return 0
    fi
  done
  echo "企业微信没能切到最前面（现在是 $(front_app)），停止操作" >&2
  exit 1
}

# 每次按键前都确认前台还是企微：焦点被别的程序抢走时，⌘A / ⌘V 会改掉别人的内容。
key() {
  [[ "$(front_app)" == "企业微信" ]] || { echo "前台变成了 $(front_app)，停止按键" >&2; exit 1; }
  osascript -e "tell application \"System Events\" to $1"
}

# 剪贴板原内容：中途因为焦点问题退出时也要还回去。
CLIP_OLD=""; CLIP_SAVED=0
restore_clip() { if (( CLIP_SAVED )); then printf '%s' "$CLIP_OLD" | pbcopy; CLIP_SAVED=0; fi; }
trap restore_clip EXIT

with_clipboard() {   # 用剪贴板做完一件事后恢复原内容
  CLIP_OLD="$(pbpaste 2>/dev/null || true)"; CLIP_SAVED=1
  "$@"
  sleep 0.4
  restore_clip
}

paste_text() { printf '%s' "$1" | pbcopy; key 'keystroke "v" using command down'; }

paste_image() {
  local cls="JPEG picture"; [[ "${1:l}" == *.png ]] && cls="«class PNGf»"
  osascript -e "set the clipboard to (read (POSIX file \"$1\") as $cls)"
  key 'keystroke "v" using command down'
}

region() {
  if [[ -n "${1:-}" ]]; then echo "$1"; return; fi
  local b; b=$(osascript -e 'tell application "System Events" to tell process "企业微信" to get {position, size} of window "企业微信"' | tr -d ' ')
  local x y w h; IFS=, read x y w h <<< "$b"
  # 2026-10-15 在这台 Mac 上实测（窗口 1153×779）：左边导航栏+会话列表约 493pt，顶部群名约 64pt，
  # 右边成员栏约 183pt，底部输入框约 229pt。拖过会话列表宽度或输入框高度后要重新截图量。
  echo "$((x+493)),$((y+64)),$((w-493-183)),$((h-64-229))"
}

case "${1:-}" in
  setup)
    if [[ ! -x "$SCROLL" ]]; then
      mkdir -p "${SCROLL:h}"
      # swiftc 和系统 SDK 版本对不上时编不过（例如 CLT 的 Swift 6.1 + macOS 26.2 SDK），改用 clang 编等价的 C 版本
      swiftc -O "$HERE/scroll.swift" -o "$SCROLL" 2>/dev/null \
        || clang -O2 -framework ApplicationServices "$HERE/scroll.c" -o "$SCROLL" \
        || echo "滚轮小工具编译失败：swiftc 和 clang 都不行，先装 Xcode Command Line Tools"
    fi
    command -v magick >/dev/null || echo "缺 ImageMagick：brew install imagemagick"
    pgrep -x 企业微信 >/dev/null || echo "企业微信没在运行"
    osascript -e 'tell application "System Events" to key code 63' >/dev/null 2>&1 && echo "辅助功能权限 OK" || echo "缺辅助功能权限：系统设置 → 隐私与安全性 → 辅助功能，打开小写的 claude"
    t=$(mktemp -t wecom).png; screencapture -x -R 0,0,10,10 "$t" && echo "截屏 OK（如果截出来是纯桌面没有窗口，就是缺「屏幕录制」权限）"; rm -f "$t"
    ;;
  bounds)
    osascript -e 'tell application "System Events" to tell process "企业微信" to get {position, size} of window "企业微信"'
    echo "默认聊天区域：$(region)"
    ;;
  search)
    raise_main
    key 'keystroke "f" using command down'; sleep 0.5
    key 'keystroke "a" using command down'
    with_clipboard paste_text "$2"
    ;;
  open)
    # 可带序号：open 2 打开第 2 条结果（按 ↓ 移过去再回车）
    raise_main
    for ((n=1; n<${2:-1}; n++)); do key 'key code 125'; sleep 0.15; done
    key 'key code 36' ;;
  shot)
    raise_main; screencapture -x -R "$(region "${3:-}")" "$2" ;;
  capture)
    [[ -x "$SCROLL" ]] || { echo "先运行 setup" >&2; exit 1; }
    out="$2"; r="$(region "${3:-}")"; step="${4:-18}"
    IFS=, read rx ry rw rh <<< "$r"; cx=$((rx+rw/2)); cy=$((ry+rh/2))
    mkdir -p "$out"; rm -f "$out"/p*.png(N) "$out"/strip_*.png(N)
    raise_main
    for k in {1..60}; do "$SCROLL" $cx $cy -40; done; sleep 1   # 先到最底部
    prev=""; same=0; i=0
    while (( i < 400 )); do
      f=$(printf "%s/p%03d.png" "$out" $i)
      screencapture -x -R "$r" "$f"
      h=$(md5 -q "$f")
      if [[ "$h" == "$prev" ]]; then
        rm "$f"; same=$((same+1)); (( same >= 3 )) && break; sleep 1.5   # 到顶时等一下，企微可能还在加载更早的消息
      else
        same=0; i=$((i+1))
      fi
      prev=$h
      "$SCROLL" $cx $cy $step; sleep 0.9
    done
    # 倒序每 3 张拼一条，strip_00 是最早的消息
    python3 - "$out" <<'EOF'
import glob, subprocess, sys
d = sys.argv[1]
fs = sorted(glob.glob(d + "/p*.png"), reverse=True)
for k in range(0, len(fs), 3):
    subprocess.run(["magick", *fs[k:k+3], "-append", "-resize", "1100x>", "%s/strip_%02d.png" % (d, k // 3)], check=True)
print("截了 %d 屏，拼成 %d 条：%s/strip_*.png" % (len(fs), (len(fs) + 2) // 3, d))
EOF
    ;;
  paste)
    draft="$(cat "${2:--}")"; [[ -n "$draft" ]] || { echo "草稿是空的" >&2; exit 1; }
    raise_main; with_clipboard paste_text "$draft"
    echo "草稿已放进当前会话输入框，没有发送。"
    ;;
  paste-image)
    raise_main
    with_clipboard paste_image "${2:A}"
    echo "图片已放进当前会话输入框，没有发送。"
    ;;
  read-input)
    raise_main
    CLIP_OLD="$(pbpaste 2>/dev/null || true)"; CLIP_SAVED=1
    printf '' | pbcopy   # 输入框为空时 ⌘C 不改剪贴板，先清空，免得读到旧内容
    key 'keystroke "a" using command down'; sleep 0.2
    key 'keystroke "c" using command down'; sleep 0.4
    key 'key code 124'
    pbpaste; echo
    restore_clip
    ;;
  send)
    raise_main; key 'key code 36'; echo "已按回车发送。" ;;
  files)
    for d in ~/Library/Containers/com.tencent.WeWorkMac/Data/Documents/Profiles/*/Caches/Files; do
      find "$d" -type f -iname "*$2*" -exec stat -f '%z  %Sm  %N' {} \; 2>/dev/null
    done
    ;;
  *)
    sed -n '2,18p' "$0"; exit 1 ;;
esac
