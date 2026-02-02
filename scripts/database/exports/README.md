# 数据库导出文件

## 文件说明

- `01_schema_full.sql` - 完整数据库结构（表、视图、索引、约束）
- `02_import_sample_data.sql` - 示例数据导入脚本
- `sample_*.csv` - 示例数据文件（每个表100条记录）

## 使用方法

### 1. 创建数据库并导入结构

```bash
# 创建数据库
createdb -U postgres npdb

# 导入结构
psql -U postgres -d npdb -f 01_schema_full.sql
```

### 2. 导入示例数据（可选）

```bash
cd exports/
psql -U postgres -d npdb -f 02_import_sample_data.sql
```

### 3. 导入完整数据

完整数据文件较大，不包含在 GitHub 仓库中。
请联系项目负责人获取完整数据文件，或使用 `/scripts/database/import_*.py` 脚本从原始数据导入。

## 注意事项

- 示例数据仅用于开发测试
- 生产环境需要导入完整数据
- 数据库用户和权限需要根据实际情况调整
