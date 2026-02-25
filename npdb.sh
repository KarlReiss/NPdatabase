#!/bin/bash
# NPdatabase 服务管理脚本
# 用法: bash npdb.sh {start|stop|restart|status|logs [frontend]}

set -e

# 配置（固定值，简单直接）
BACKEND_PORT=8080
FRONTEND_PORT=3001
DB_USER=yfguo
DB_PASSWORD=npdb2024

# 路径
ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend/web"
BACKEND_LOG="$BACKEND_DIR/logs/backend.log"
FRONTEND_LOG="$FRONTEND_DIR/logs/frontend.log"
BACKEND_PID="$BACKEND_DIR/run/backend.pid"
FRONTEND_PID="$FRONTEND_DIR/run/frontend.pid"

# 确保目录存在
mkdir -p "$BACKEND_DIR/logs" "$BACKEND_DIR/run" "$FRONTEND_DIR/logs" "$FRONTEND_DIR/run"

# 检查服务是否运行
is_running() {
    local pid_file=$1
    [[ -f "$pid_file" ]] && kill -0 "$(cat "$pid_file")" 2>/dev/null
}

# 等待后端启动
wait_backend() {
    for i in {1..30}; do
        if curl -sf "http://localhost:$BACKEND_PORT/api/stats/overview" >/dev/null 2>&1; then
            return 0
        fi
        sleep 2
    done
    return 1
}

# 启动后端
start_backend() {
    if is_running "$BACKEND_PID"; then
        echo "后端已在运行，PID: $(cat $BACKEND_PID)"
        return 0
    fi

    echo "编译后端..."
    cd "$BACKEND_DIR"
    mvn package -DskipTests -q || { echo "✗ 编译失败"; return 1; }

    echo "启动后端服务..."
    DB_USER=$DB_USER DB_PASSWORD=$DB_PASSWORD \
        nohup java -jar "$BACKEND_DIR/target/backend-0.1.0-SNAPSHOT.jar" > "$BACKEND_LOG" 2>&1 &
    echo $! > "$BACKEND_PID"
    
    if wait_backend; then
        echo "✓ 后端启动成功"
        echo "  API: http://localhost:$BACKEND_PORT"
        echo "  Swagger: http://localhost:$BACKEND_PORT/swagger-ui.html"
    else
        echo "✗ 后端启动失败，查看日志: $BACKEND_LOG"
        tail -50 "$BACKEND_LOG"
        return 1
    fi
}

# 启动前端
start_frontend() {
    if is_running "$FRONTEND_PID"; then
        echo "前端已在运行，PID: $(cat $FRONTEND_PID)"
        return 0
    fi
    
    echo "启动前端服务..."
    cd "$FRONTEND_DIR"
    nohup npm run dev -- --host 0.0.0.0 --port $FRONTEND_PORT > "$FRONTEND_LOG" 2>&1 &
    echo $! > "$FRONTEND_PID"
    sleep 3
    
    if is_running "$FRONTEND_PID"; then
        echo "✓ 前端启动成功"
        echo "  访问: http://localhost:$FRONTEND_PORT"
    else
        echo "✗ 前端启动失败，查看日志: $FRONTEND_LOG"
        return 1
    fi
}

# 停止后端（需同时杀 mvn 父进程和 java 子进程）
stop_backend_proc() {
    echo "停止后端..."
    pkill -f "spring-boot:run" 2>/dev/null || true
    pkill -f "NpdbApplication\|backend-0.1.0-SNAPSHOT.jar" 2>/dev/null || true
    sleep 2
    # 兜底：按端口强杀
    local pid
    pid=$(ss -tlnp 2>/dev/null | grep ":$BACKEND_PORT " | grep -oP 'pid=\K[0-9]+' | head -1)
    [[ -n "$pid" ]] && kill -9 "$pid" 2>/dev/null || true
    rm -f "$BACKEND_PID"
    echo "✓ 后端已停止"
}

# 停止前端
stop_frontend_proc() {
    echo "停止前端..."
    if [[ -f "$FRONTEND_PID" ]]; then
        local pid
        pid=$(cat "$FRONTEND_PID")
        kill "$pid" 2>/dev/null || true
        sleep 2
        kill -9 "$pid" 2>/dev/null || true
    fi
    pkill -f "vite\|npm.*dev" 2>/dev/null || true
    rm -f "$FRONTEND_PID"
    echo "✓ 前端已停止"
}

# 显示状态
show_status() {
    echo "=========================================="
    echo "NPdatabase 服务状态"
    echo "=========================================="
    
    if is_running "$BACKEND_PID"; then
        echo "✓ 后端运行中 (PID: $(cat $BACKEND_PID), 端口: $BACKEND_PORT)"
    else
        echo "✗ 后端未运行"
    fi
    
    if is_running "$FRONTEND_PID"; then
        echo "✓ 前端运行中 (PID: $(cat $FRONTEND_PID), 端口: $FRONTEND_PORT)"
    else
        echo "✗ 前端未运行"
    fi
    
    echo "=========================================="
}

# 显示帮助
show_help() {
    cat << EOF
NPdatabase 服务管理脚本

用法: bash npdb.sh <命令>

命令:
  start           启动前后端服务
  stop            停止前后端服务
  restart         重启前后端服务
  status          查看服务状态
  logs            查看后端日志
  logs frontend   查看前端日志

访问地址:
  前端页面: http://localhost:$FRONTEND_PORT
  API文档:  http://localhost:$BACKEND_PORT/swagger-ui.html

示例:
  bash npdb.sh start    # 启动服务
  bash npdb.sh status   # 查看状态
  bash npdb.sh logs     # 查看日志
EOF
}

# 主逻辑
case "${1:-}" in
    start)
        start_backend
        start_frontend
        echo ""
        echo "启动完成！访问 http://localhost:$FRONTEND_PORT"
        ;;
    stop)
        stop_frontend_proc
        stop_backend_proc
        ;;
    restart)
        bash "$ROOT_DIR/npdb.sh" stop
        sleep 2
        bash "$ROOT_DIR/npdb.sh" start
        ;;
    status)
        show_status
        ;;
    logs)
        if [[ "${2:-}" == "frontend" ]]; then
            tail -100 -f "$FRONTEND_LOG" 2>/dev/null || echo "日志文件不存在"
        else
            tail -100 -f "$BACKEND_LOG" 2>/dev/null || echo "日志文件不存在"
        fi
        ;;
    -h|--help|*)
        show_help
        ;;
esac
