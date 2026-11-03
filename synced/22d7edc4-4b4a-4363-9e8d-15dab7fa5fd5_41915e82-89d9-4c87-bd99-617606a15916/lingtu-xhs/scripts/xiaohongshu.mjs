#!/usr/bin/env node

/**
 * 凌图小红书 skill 统一入口
 */

import { spawnSync } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';

const here = dirname(fileURLToPath(import.meta.url));
const [command, ...rest] = process.argv.slice(2);
const param = rest.join(' ');

const scripts = { post: 'generate_post.mjs', hot: 'hot_words.mjs', check: 'check_violation.mjs' };

if (!scripts[command]) {
  console.log(`
凌图小红书 skill

用法：node xiaohongshu.mjs <命令> "<参数>"

  post  <主题>   输出笔记骨架
  hot   <主题>   关键词候选（不联网，无热度数据）
  check <文本>   合规检查

示例：
  node xiaohongshu.mjs check "全网第一的移民律师，保证获批"
`);
  process.exit(0);
}

const r = spawnSync(process.execPath, [join(here, scripts[command]), param], { stdio: 'inherit' });
process.exit(r.status ?? 1);
