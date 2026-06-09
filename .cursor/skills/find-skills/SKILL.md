---
name: find-skills
description: 发现、安装和管理Cursor技能。当用户想要查找可用技能、从GitHub添加技能、浏览技能仓库、管理已安装的技能、或询问如何获取新技能时使用。
---

# Find Skills - Cursor技能管理

这个技能帮助你发现、安装和管理Cursor的Agent Skills。

## 快速开始

### 发现技能

从官方或社区仓库浏览可用的技能:

```bash
# 从Vercel Labs技能仓库查找
npx skills add https://github.com/vercel-labs/skills --skill find-skills

# 从其他社区仓库查找
npx skills add https://github.com/username/cursor-skills --skill skill-name
```

### 安装技能

```bash
# 安装单个技能
npx skills add <github-repo-url> --skill <skill-name>

# 安装仓库中的所有技能
npx skills add <github-repo-url>
```

## 主要功能

### 1. 查找可用技能

**官方技能仓库:**
- [Vercel Labs Skills](https://github.com/vercel-labs/skills) - Vercel官方维护的技能集合
- 包含各种实用技能:代码审查、提交消息生成、文档生成等

**社区技能仓库:**
- 搜索GitHub上的 `cursor-skills` 或 `cursor-agent-skills` 标签
- 查找其他开发者分享的技能

**浏览技能内容:**
访问GitHub仓库,查看README和各个技能目录,了解:
- 技能的用途和功能
- 使用示例
- 安装说明

### 2. 安装技能

**从GitHub安装:**

```bash
# 基本语法
npx skills add <repo-url> --skill <skill-name>

# 示例:安装代码审查技能
npx skills add https://github.com/vercel-labs/skills --skill code-review

# 示例:安装提交消息生成器
npx skills add https://github.com/vercel-labs/skills --skill commit-message
```

**批量安装:**

```bash
# 安装仓库中的所有技能
npx skills add https://github.com/vercel-labs/skills
```

**选择安装位置:**
- **个人技能** (默认): 安装到 `~/.cursor/skills/`
- **项目技能**: 安装到项目的 `.cursor/skills/`

```bash
# 安装为项目技能(推荐用于团队共享)
cd /path/to/your/project
npx skills add <repo-url> --skill <skill-name>
# 技能将安装到当前项目的.cursor/skills/目录
```

### 3. 管理已安装的技能

**查看已安装的技能:**

```bash
# 列出个人技能
ls -la ~/.cursor/skills/

# 列出项目技能
ls -la .cursor/skills/
```

**更新技能:**

```bash
# 重新运行安装命令即可更新
npx skills add <repo-url> --skill <skill-name>
```

**删除技能:**

```bash
# 删除个人技能
rm -rf ~/.cursor/skills/skill-name/

# 删除项目技能
rm -rf .cursor/skills/skill-name/
```

**编辑技能:**

直接编辑技能目录中的 `SKILL.md` 文件,根据你的需求自定义:

```bash
# 编辑个人技能
cursor ~/.cursor/skills/skill-name/SKILL.md

# 编辑项目技能
cursor .cursor/skills/skill-name/SKILL.md
```

## 常用技能推荐

### 代码质量类
- **code-review** - 代码审查和质量检查
- **refactor** - 代码重构建议
- **test-generation** - 生成单元测试

### 文档类
- **commit-message** - 生成规范的提交消息
- **documentation** - 生成代码文档
- **changelog** - 生成变更日志

### 工具类
- **debug** - 调试辅助
- **performance** - 性能分析
- **security-audit** - 安全审计

## 使用示例

### 示例1: 为项目添加代码审查技能

```bash
# 进入项目目录
cd /Users/ruanjunwei/Documents/rjw_gitee/supatable

# 安装代码审查技能到项目
npx skills add https://github.com/vercel-labs/skills --skill code-review

# 现在可以在代码审查时触发此技能
# Agent会自动应用代码审查标准
```

### 示例2: 安装提交消息生成器

```bash
# 安装到个人技能目录
cd ~
npx skills add https://github.com/vercel-labs/skills --skill commit-message

# 当你准备提交代码时,Agent会帮助生成规范的提交消息
```

### 示例3: 浏览和选择技能

```bash
# 1. 先浏览官方仓库
# 在浏览器中打开: https://github.com/vercel-labs/skills

# 2. 查看README,了解可用技能列表

# 3. 选择需要的技能并安装
npx skills add https://github.com/vercel-labs/skills --skill <chosen-skill>
```

## 技能工作原理

### 技能发现机制
- Agent会自动扫描 `~/.cursor/skills/` 和 `.cursor/skills/` 目录
- 读取每个技能的 `SKILL.md` 文件
- 根据 `description` 字段判断何时应用该技能

### 触发条件
技能会在以下情况自动触发:
1. 用户请求与技能描述匹配
2. Agent检测到相关的任务类型
3. 用户明确提到技能名称

### 优先级
- 项目技能 (`.cursor/skills/`) 优先于个人技能
- 多个匹配技能时,Agent会选择最相关的
- 可以通过重命名技能目录来临时禁用(添加 `.disabled` 后缀)

## 创建自己的技能

如果找不到合适的技能,可以创建自定义技能:

```bash
# 使用create-skill命令创建
# 在Cursor中输入:
/create-skill
```

参考 [创建技能指南](https://docs.cursor.com/skills/creating-skills) 了解详细信息。

## 故障排查

### 技能未生效
1. **检查技能位置**: 确认技能在正确的目录
2. **检查SKILL.md格式**: 确保YAML frontmatter格式正确
3. **检查description**: 描述要足够具体,包含触发关键词
4. **重启Cursor**: 有时需要重启以重新加载技能

### 安装失败
1. **网络连接**: 确保能访问GitHub
2. **权限问题**: 检查目录写入权限
3. **npx版本**: 确保Node.js和npm已安装

### 技能冲突
- 如果多个技能功能重叠,可能导致不确定行为
- 建议禁用或删除不需要的技能
- 确保技能描述清晰区分用途

## 最佳实践

### 技能选择
1. **从官方开始**: 优先使用官方技能,质量有保证
2. **按需安装**: 不要一次性安装太多技能
3. **定期清理**: 删除不常用的技能,保持环境整洁

### 技能组织
1. **团队共享**: 将团队通用技能安装到项目目录
2. **个人偏好**: 将个人习惯的技能安装到个人目录
3. **版本控制**: 将项目技能加入Git,与团队同步

### 技能维护
1. **定期更新**: 检查技能更新,获取新功能
2. **自定义调整**: 根据团队需求调整技能内容
3. **文档记录**: 在项目README中说明已安装的技能

## 相关资源

- [Cursor官方文档](https://docs.cursor.com)
- [Vercel Labs Skills仓库](https://github.com/vercel-labs/skills)
- [创建技能指南](https://docs.cursor.com/skills/creating-skills)
- [技能最佳实践](https://docs.cursor.com/skills/best-practices)

## 注意事项

1. **安全性**: 只从可信的来源安装技能
2. **审查代码**: 安装前查看技能内容,确保无恶意代码
3. **备份**: 修改技能前备份原始文件
4. **测试**: 在测试项目中先试用新技能
5. **文档**: 记录自定义修改,便于维护

---

**提示**: 这个技能本身也可以作为示例,参考它的结构来创建你自己的技能!
