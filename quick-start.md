# NPdatabase 快速启动卡片

## 🎯 一键启动

```bash
cd /home/yfguo/NPdatabase
bash scripts/backend-service.sh start
```

等待 1-2 分钟后访问：
- **前端页面**：http://localhost:3001
- **API文档**：http://localhost:8080/swagger-ui.html

## 📋 常用命令

| 命令 | 说明 |
|------|------|
| `bash scripts/backend-service.sh start` | 启动服务 |
| `bash scripts/backend-service.sh stop` | 停止服务 |
| `bash scripts/backend-service.sh restart` | 重启服务 |
| `bash scripts/backend-service.sh status` | 查看状态 |
| `bash scripts/backend-service.sh logs` | 查看后端日志 |
| `bash scripts/backend-service.sh logs frontend` | 查看前端日志 |

## 🔧 默认配置

- **后端端口**：8080
- **前端端口**：3001
- **数据库用户**：yfguo
- **数据库密码**：npdb2024

## ❗ 遇到问题？

1. **端口被占用**：脚本会自动清理，如果失败请先执行 `stop` 再 `start`
2. **数据库连接失败**：检查 PostgreSQL 是否运行
3. **查看详细日志**：使用 `logs` 命令查看错误信息

详细说明请查看：[完整启动指南](startup-guide.md)
