#!/bin/bash

# NPASS 结构数据导入脚本
# 用法: ./import_npass_structures.sh

set -e

DB_HOST="localhost"
DB_PORT="5432"
DB_NAME="npdb"
DB_USER="yfguo"
DB_PASSWORD="npdb2024"

DATA_FILE="/home/yfguo/NPdatabase/data/NPASS/NPASS3.0_naturalproducts_structure.txt"
TEMP_FILE="/tmp/npass_structures_import.csv"

echo "开始处理 NPASS 结构数据..."

# 跳过第一行标题，转换为 CSV 格式
tail -n +2 "$DATA_FILE" | awk -F'\t' '{
    # 转义单引号和反斜杠
    gsub(/'\''/, "'\'''\''", $1);
    gsub(/'\''/, "'\'''\''", $2);
    gsub(/'\''/, "'\'''\''", $3);
    gsub(/'\''/, "'\'''\''", $4);
    print $1 "\t" $2 "\t" $3 "\t" $4
}' > "$TEMP_FILE"

echo "数据文件已准备完成，开始导入数据库..."

# 使用 COPY 命令批量导入
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" << EOF
-- 清空现有数据（如果需要）
-- TRUNCATE TABLE npass_structures;

-- 批量导入数据
COPY npass_structures (np_id, inchi, inchikey, smiles)
FROM '$TEMP_FILE'
WITH (FORMAT text, DELIMITER E'\t', NULL '');

-- 更新时间戳
UPDATE npass_structures SET updated_at = CURRENT_TIMESTAMP WHERE updated_at IS NULL;

-- 显示导入统计
SELECT COUNT(*) as total_records FROM npass_structures;
EOF

echo "数据导入完成！"

# 清理临时文件
rm -f "$TEMP_FILE"
