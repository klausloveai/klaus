#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一个已发布的 case artifact 刷到当前 shell。

只换 <style>、结尾的 <script> 和 data-shell 版本戳，正文一个字不动。
所以它只能处理「样式变了」，处理不了「正文结构变了」—— 大版本变动仍要人工过一遍
（见 SKILL.md 的「版本号」一节）。

    python3 scripts/reskin.py <存到本地的页面.html>          # 就地改写
    python3 scripts/reskin.py --check <存到本地的页面.html>   # 只报版本，不写

调用方式：用 Artifact read 带 `path` 把页面存到磁盘（这样 40 KB 的 HTML 不会进对话），
跑这个脚本，再 publish 回同一个 url。
"""
import re, sys, os

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHELL = os.path.join(HERE, 'assets', 'shell.html')


def block(text, tag):
    m = re.search(r'<%s>.*?</%s>' % (tag, tag), text, re.S)
    return m.group(0) if m else None


def stamp(text):
    m = re.search(r'data-shell="([\d.]+)"', text)
    return m.group(1) if m else None


def main():
    args = [a for a in sys.argv[1:] if a not in ('--check', '--css-only')]
    check = '--check' in sys.argv
    if not args:
        print(__doc__)
        sys.exit(2)
    page_path = args[0]
    shell = open(SHELL, encoding='utf-8').read()
    page = open(page_path, encoding='utf-8').read()
    want, have = stamp(shell), stamp(page)
    print('shell %s  |  page %s  |  %s' % (
        want, have or '(无戳，视为旧版)', '已是最新' if have == want else '需要刷新'))
    if check or have == want:
        if have and have.split('.')[0] != want.split('.')[0]:
            print('  [大版本] 正文结构也变了，脚本只换样式；加 --css-only 才执行，正文缺的节下次动该页时人工补')
        return
    if have and have.split('.')[0] != want.split('.')[0] and '--css-only' not in sys.argv:
        print('  [停] 大版本 %s → %s：脚本只能换样式。确认只要样式就加 --css-only；'
              '版本戳会写成 %s 并在 applied.json 里记 "%s-css"' % (have, want, want, want))
        sys.exit(1)
    for tag in ('style', 'script'):
        new, old = block(shell, tag), block(page, tag)
        if new is None:
            print('  [warn] shell 里没有 <%s>' % tag); continue
        if old is None:
            print('  [warn] 页面里没有 <%s>，跳过' % tag); continue
        page = page.replace(old, new, 1)
    if have:
        page = re.sub(r'data-shell="[\d.]+"', 'data-shell="%s"' % want, page, count=1)
    else:
        page = page.replace('<div class="wrap">',
                            '<div class="wrap" data-shell="%s">' % want, 1)
    open(page_path, 'w', encoding='utf-8').write(page)
    print('  已刷到 %s —— 正文未动，publish 回同一个 url 即可' % want)


if __name__ == '__main__':
    main()
