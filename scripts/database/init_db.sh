#!/bin/bash
# Natural Product Database - 数据库初始化脚本

set -e

DB_NAME="${DB_NAME:-npdb}"
DB_USER="${DB_USER:-yfguo}"
DB_PASSWORD="${DB_PASSWORD:-npdb2024}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCHEMA_FILE="${SCRIPT_DIR}/exports/01_schema_full.sql"

echo "=========================================="
echo "Natural Product Database - 数据库初始化"
echo "=========================================="
echo ""
echo "配置信息:"
echo "  数据库名: $DB_NAME"
echo "  用户名: $DB_USER"
echo "  主机: $DB_HOST"
echo "  端口: $DB_PORT"
echo ""

if ! command -v psql &> /dev/null; then
    echo "错误: PostgreSQL 未安装"
    exit 1
fi

echo "✓ PostgreSQL 已安装"

if ! pg_isready -h "$DB_HOST" -p "$DB_PORT" &> /dev/null; then
    echo "错误: PostgreSQL 服务未运行"
    echo "启动命令: sudo systemctl start postgresql"
    exit 1
fi

echo "✓ PostgreSQL 服务正在运行"

if [ ! -f "$SCHEMA_FILE" ]; then
    echo "错误: Schema 文件不存在: $SCHEMA_FILE"
    exit 1
fi

echo "✓ Schema 文件存在"
echo ""

export PGPASSWORD="$DB_PASSWORD"

read -p "是否删除已存在的数据库 '$DB_NAME'? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在删除数据库 '$DB_NAME'..."
    dropdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" --if-exists "$DB_NAME" 2>/dev/null || {
        dropdb -h "$DB_HOST" -p "$DB_PORT" -U postgres --if-exists "$DB_NAME" 2>/dev/null || true
    }
    echo "✓ 数据库已删除"
fi

echo ""
echo "正在创建数据库 '$DB_NAME'..."
createdb -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" "$DB_NAME" 2>/dev/null || {
    createdb -h "$DB_HOST" -p "$DB_PORT" -U postgres -O "$DB_USER" "$DB_NAME"
}
echo "✓ 数据库创建成功"

echo ""
echo "正在执行建表脚本..."
psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME" -f "$SCHEMA_FILE"

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 数据库初始化完成！"
    echo "=========================================="
    echo ""
    echo "下一步: 导入数据（如需重新导入）"
    echo "  数据文件位于 data/ 目录"
    echo ""
else
    echo ""
    echo "建表脚本执行失败"
    unset PGPASSWORD
    exit 1
fi

unset PGPASSWORD
