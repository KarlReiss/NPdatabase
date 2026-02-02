#!/bin/bash
# ============================================
# 数据库初始化脚本
# ============================================

set -e  # 遇到错误立即退出

# 配置变量
DB_NAME="npdb"
DB_USER="postgres"
DB_HOST="localhost"
DB_PORT="5432"

echo "=========================================="
echo "Natural Product Database - 数据库初始化"
echo "=========================================="
echo ""

# 检查 PostgreSQL 是否安装
if ! command -v psql &> /dev/null; then
    echo "❌ 错误: PostgreSQL 未安装"
    echo "请先安装 PostgreSQL: https://www.postgresql.org/download/"
    exit 1
fi

echo "✓ PostgreSQL 已安装"

# 检查 PostgreSQL 是否运行
if ! pg_isready -h $DB_HOST -p $DB_PORT &> /dev/null; then
    echo "❌ 错误: PostgreSQL 服务未运行"
    echo "请启动 PostgreSQL 服务"
    exit 1
fi

echo "✓ PostgreSQL 服务正在运行"
echo ""

# 询问是否删除已存在的数据库
read -p "是否删除已存在的数据库 '$DB_NAME'? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "正在删除数据库 '$DB_NAME'..."
    dropdb -h $DB_HOST -p $DB_PORT -U $DB_USER --if-exists $DB_NAME
    echo "✓ 数据库已删除"
fi

# 创建数据库
echo ""
echo "正在创建数据库 '$DB_NAME'..."
createdb -h $DB_HOST -p $DB_PORT -U $DB_USER $DB_NAME
echo "✓ 数据库创建成功"

# 执行建表脚本
echo ""
echo "正在执行建表脚本..."
psql -h $DB_HOST -p $DB_PORT -U $DB_USER -d $DB_NAME -f schema.sql

if [ $? -eq 0 ]; then
    echo ""
    echo "=========================================="
    echo "✓ 数据库初始化完成！"
    echo "=========================================="
    echo ""
    echo "数据库信息:"
    echo "  名称: $DB_NAME"
    echo "  主机: $DB_HOST"
    echo "  端口: $DB_PORT"
    echo "  用户: $DB_USER"
    echo ""
    echo "下一步:"
    echo "  1. 运行数据导入脚本: cd ../data-import && python import_all.py"
    echo "  2. 验证数据: psql -d $DB_NAME -c 'SELECT COUNT(*) FROM compounds;'"
    echo ""
else
    echo ""
    echo "❌ 建表脚本执行失败"
    exit 1
fi
