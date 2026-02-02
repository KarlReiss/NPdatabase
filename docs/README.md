# 项目文档目录

## 文档说明

### database.md
**数据库结构说明** - 基于当前建表脚本与结构优化脚本的最终数据库说明

**适用场景**:
- 后端开发数据库字段对照
- 数据工程/导入与维护参考
- 查询与视图使用说明

**核心内容**:
- 最终表结构（natural_products/bio_resources/prescriptions 等）
- 旧表名到新表名映射
- 视图与触发器说明
- 常用查询与维护 SQL

### requirements-simplified.md
**简化版需求文档** - 基于现有界面原型和 NPASS 3.0 数据的实际需求

**适用场景**:
- 快速了解项目核心功能
- 开发实现参考
- 一期开发范围

**核心内容**:
- 化合物、活性、靶点三大核心实体
- 基础浏览、检索、筛选功能
- 详情页与关联跳转
- 专题库（抗肿瘤、心脑血管、有毒药材）

### archived/requirements-full.md
**完整版需求文档** - 包含所有规划功能的详细需求（已归档）

**适用场景**:
- 了解项目长期规划
- 二期功能扩展参考
- 完整的数据模型设计

**额外内容**:
- 方剂、证候、通路、疾病映射
- LC-MS/组学数据
- 管理后台与数据审核
- 权限管理与导出功能

### archived/2026-01-29/next-steps-2026-01-29.md
**历史计划文档** - 后端完成前的阶段计划（已归档）

### backend-plan.md
**后端开发检查清单** - 面向非程序员的逐步验收清单

### backend-dev-doc.md
**后端开发文档** - 代码结构、配置、API 与维护说明

### backend-dev-log.md
**后端开发日志** - 关键节点、问题修复与验证记录

### backend-acceptance.md
**后端验收记录表** - 可直接填写的验收表格

### backend-delivery.md
**后端交付说明** - 交付物清单、启动方式、Swagger 入口与验证接口示例

### swagger-validation.md
**Swagger 校验说明** - 给非开发人员的操作步骤

## 建议阅读顺序

1. **开发人员**: 先读 `requirements-simplified.md`，了解一期实现范围
2. **后端维护**: 阅读 `backend-dev-doc.md` 与 `backend-dev-log.md`
3. **产品经理**: 两份需求文档都要读，了解完整规划
4. **数据工程师**: 重点关注数据模型部分和 `../data/` 目录
5. **验收人员**: 阅读 `backend-plan.md` 与 `backend-acceptance.md`

## 相关目录

- `/data` - NPASS 3.0 原始数据文件
- `/docs/archived/reference` - 参考网站和资料
- `/docs/archived/2026-01-29` - 已归档的历史计划文档
- `/docs` - 项目文档（当前目录）
