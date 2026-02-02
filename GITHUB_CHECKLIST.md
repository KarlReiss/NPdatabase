# GitHub 上传前检查清单

## ✅ 准备工作

### 1. 文件结构检查

- [x] `.gitignore` 已创建（排除大文件和敏感信息）
- [x] `SETUP.md` 已创建（环境设置指南）
- [x] `data/README.md` 已创建（数据获取说明）
- [x] 数据库结构已导出到 `scripts/database/exports/`
- [x] README.md 已更新

### 2. 敏感信息检查

- [ ] 确认没有硬编码的密码
- [ ] 确认没有 API 密钥
- [ ] 确认没有个人信息
- [ ] 检查 `application.yml` 中的配置（应使用环境变量）

### 3. 大文件检查

以下文件/文件夹已在 `.gitignore` 中排除：

- [x] `/data/CMAUP/` (442MB)
- [x] `/data/NPASS/` (331MB)
- [x] `/data/TCMID/` (1.5MB)
- [x] `/data/TTD/` (7.3MB)
- [x] `/backups/*.sql` (344MB)
- [x] `backend/target/`
- [x] `frontend/web/node_modules/`

### 4. 文档完整性

- [x] README.md - 项目概述
- [x] SETUP.md - 环境设置
- [x] CLAUDE.md - AI 开发指南
- [x] docs/database.md - 数据库文档
- [x] docs/backend-dev-doc.md - 后端文档
- [x] data/README.md - 数据获取说明
- [x] scripts/database/exports/README.md - 数据库导出说明

## 📋 上传步骤

### 1. 初始化 Git 仓库

```bash
cd /home/yfguo/NPdatabase

# 初始化 Git
git init

# 添加所有文件
git add .

# 查看将要提交的文件
git status
```

### 2. 检查是否有不应该提交的文件

```bash
# 查看暂存区文件大小
git ls-files -s | awk '{print $4, $2}' | sort -k2 -n -r | head -20

# 如果发现大文件，添加到 .gitignore
```

### 3. 创建首次提交

```bash
git commit -m "Initial commit: NPdatabase project

- Backend: Spring Boot + MyBatis-Plus (completed)
- Frontend: Vue 3 + TypeScript (in progress)
- Database: PostgreSQL schema and sample data
- Documentation: Setup guide, API docs, database schema
"
```

### 4. 连接到 GitHub 仓库

```bash
# 在 GitHub 上创建新仓库后，执行：
git remote add origin <your-github-repo-url>

# 推送到 GitHub
git branch -M main
git push -u origin main
```

## ⚠️ 重要提醒

### 数据文件处理

**不要上传原始数据文件到 GitHub！**

原因：
1. 文件太大（~780MB）会导致仓库臃肿
2. GitHub 有单文件 100MB 限制
3. 数据可能有版权限制

**替代方案：**
1. 使用 Git LFS（如果必须上传大文件）
2. 提供数据下载链接（推荐）
3. 使用云存储（Google Drive, Dropbox 等）
4. 使用示例数据（已导出到 `scripts/database/exports/`）

### 数据库备份

`/backups/` 文件夹中的 SQL 备份文件（344MB）已被排除。

团队成员应该：
1. 使用 `scripts/database/exports/01_schema_full.sql` 创建结构
2. 使用 `scripts/database/exports/02_import_sample_data.sql` 导入示例数据
3. 或从原始数据源重新导入完整数据

## 🔍 验证清单

上传后，让团队成员测试：

- [ ] 克隆仓库
- [ ] 按照 SETUP.md 设置环境
- [ ] 成功启动后端
- [ ] 成功启动前端
- [ ] API 正常工作
- [ ] 文档清晰易懂

## 📝 后续维护

### 分支策略建议

```
main        - 稳定版本
develop     - 开发分支
feature/*   - 功能分支
bugfix/*    - 修复分支
```

### 提交信息规范

```
feat: 新功能
fix: 修复
docs: 文档
style: 格式
refactor: 重构
test: 测试
chore: 构建/工具
```

## 🎯 团队协作建议

1. **代码审查**: 使用 Pull Request 进行代码审查
2. **Issue 跟踪**: 使用 GitHub Issues 跟踪任务和 bug
3. **文档更新**: 代码变更时同步更新文档
4. **环境变量**: 使用 `.env.example` 文件提供配置模板
5. **依赖管理**: 定期更新依赖并测试兼容性

## ✅ 完成

上传完成后：
1. 在 GitHub 仓库添加项目描述
2. 添加 Topics 标签（如：natural-products, spring-boot, vue3, postgresql）
3. 设置仓库可见性（public/private）
4. 邀请团队成员
5. 设置分支保护规则（可选）
