# 数据文件说明

## 📁 文件夹结构

```
data/
├── CMAUP/      # 442MB - 中药分子数据库
├── NPASS/      # 331MB - 天然产物数据库（主要数据源）
├── TCMID/      # 1.5MB - 中药成分数据库
└── TTD/        # 7.3MB - 治疗靶点数据库
```

## ⚠️ 重要说明

由于数据文件较大（总计约 780MB），**不包含在 GitHub 仓库中**。

## 📥 如何获取数据文件

### 方案 1：从原始来源下载（推荐）

- **NPASS 3.0**: https://bidd.group/NPASS/
- **CMAUP**: https://bidd.group/CMAUP/
- **TCMID**: http://www.megabionet.org/tcmid/
- **TTD**: http://db.idrblab.net/ttd/

### 方案 2：从团队共享获取

请联系项目负责人获取数据文件压缩包。

### 方案 3：使用示例数据

如果只是开发测试，可以使用 `/scripts/database/exports/` 中的示例数据。

## 🔧 数据导入

下载数据文件后，将其放置在对应文件夹中，然后运行导入脚本：

```bash
# 导入 NPASS 数据（主要数据源）
python scripts/database/import_natural_products.py
python scripts/database/import_targets.py
python scripts/database/import_bioactivity.py
python scripts/database/import_toxicity.py
python scripts/database/import_bio_resources.py
python scripts/database/import_bio_resource_natural_products.py
```

## 📊 数据统计

- Natural Products: ~500,000 条
- Bioactivity Records: ~1,000,000 条
- Targets: ~1,000 条
- Bio Resources: ~10,000 条

## 🔒 数据使用许可

请遵守各数据库的使用条款和引用要求。
