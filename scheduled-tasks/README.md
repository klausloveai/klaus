# scheduled-tasks（定时 routine，版本化备份）

**真实目录就在这里**；`~/.claude/scheduled-tasks` 是指向本目录的**符号链接**：

```
~/.claude/scheduled-tasks -> skills/scheduled-tasks
```

Cowork 的 scheduled-tasks MCP 通过那个链接读写 `{taskId}/SKILL.md`，所以改 routine
照常用 app 或直接编辑这里的文件，两边是同一份。

## 为什么放进 git

这些 routine 是**无人值守运行**的：`hourly-email-agent` 工作日每小时跑一次、会打 Gmail
label 和建草稿，`hernan-case-daily-sync` 每天往各案 Case Log 写字。它们和 skills 属于
同一类资产（沉淀下来的流程知识），却是系统里**唯一没有撤销键**的部分 —— 改坏了不会报错，
只会安静地每小时产出错东西，而且没有历史可以比对"上周它到底是怎么写的"。

## 注意

- **别把这个目录移走或重建** —— 那会打断符号链接，app 会认为一个 routine 都没有。
  自检：`readlink -f ~/.claude/scheduled-tasks` 应当指到本目录。
- 每次改完 routine 记得 commit + push（同 skills 的规矩）。
- **仓库内不放任何凭据**；routine 里只写资源 id（spreadsheetId、label id、space id 之类），
  认证一律走本机 keyring 的 gws。
