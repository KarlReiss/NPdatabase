#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_NAME_BACKEND="npdb-backend"
APP_NAME_FRONTEND="npdb-frontend"
BACKEND_PID_FILE="$ROOT_DIR/backend/run/backend.pid"
BACKEND_LOG_FILE="$ROOT_DIR/backend/logs/backend.log"
FRONTEND_DIR="$ROOT_DIR/frontend/web"
FRONTEND_PID_FILE="$ROOT_DIR/frontend/web/run/frontend.pid"
FRONTEND_LOG_FILE="$ROOT_DIR/frontend/web/logs/frontend.log"

DB_USER_VALUE="${DB_USER:-yfguo}"
DB_PASSWORD_VALUE="${DB_PASSWORD:-npdb2024}"
SPRING_PROFILE_VALUE="${SPRING_PROFILES_ACTIVE:-}"
SERVER_ADDRESS_VALUE="${SERVER_ADDRESS:-0.0.0.0}"
SERVER_PORT_VALUE="${SERVER_PORT:-8080}"
FRONTEND_HOST_VALUE="${FRONTEND_HOST:-0.0.0.0}"
FRONTEND_PORT_VALUE="${FRONTEND_PORT:-3001}"

MVN_CMD=(mvn -f "$ROOT_DIR/backend/pom.xml" spring-boot:run -DskipTests)
NPM_CMD=(npm --prefix "$FRONTEND_DIR" run dev -- --host "$FRONTEND_HOST_VALUE" --port "$FRONTEND_PORT_VALUE")

ensure_dirs() {
  mkdir -p "$(dirname "$BACKEND_PID_FILE")" "$(dirname "$BACKEND_LOG_FILE")"
  mkdir -p "$(dirname "$FRONTEND_PID_FILE")" "$(dirname "$FRONTEND_LOG_FILE")"
}

wait_for_backend() {
  local url="http://localhost:${SERVER_PORT_VALUE}/api/health"
  local retries=20
  local wait_seconds=1

  for _ in $(seq 1 "$retries"); do
    if curl -sf "$url" >/dev/null 2>&1; then
      return 0
    fi
    sleep "$wait_seconds"
  done
  return 1
}

# 检查端口是否被占用
check_port() {
  local port=$1
  if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
    return 0  # 端口被占用
  else
    return 1  # 端口空闲
  fi
}

# 杀死占用指定端口的进程
kill_port() {
  local port=$1
  local service_name=$2

  if check_port "$port"; then
    echo "检测到端口 $port 被占用，正在清理..."
    local pids=$(lsof -ti :$port)
    if [[ -n "$pids" ]]; then
      echo "发现占用端口 $port 的进程: $pids"
      for pid in $pids; do
        echo "终止进程 $pid..."
        kill -15 "$pid" 2>/dev/null || true
      done

      # 等待进程退出
      sleep 2

      # 如果还在运行，强制终止
      if check_port "$port"; then
        echo "进程未退出，强制终止..."
        for pid in $pids; do
          kill -9 "$pid" 2>/dev/null || true
        done
        sleep 1
      fi

      if check_port "$port"; then
        echo "警告：端口 $port 仍被占用，$service_name 可能无法启动"
        return 1
      else
        echo "端口 $port 已释放"
      fi
    fi
  fi
  return 0
}

is_running_backend() {
  if [[ -f "$BACKEND_PID_FILE" ]]; then
    local pid
    pid="$(cat "$BACKEND_PID_FILE")"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

is_running_frontend() {
  if [[ -f "$FRONTEND_PID_FILE" ]]; then
    local pid
    pid="$(cat "$FRONTEND_PID_FILE")"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

start_backend() {
  if is_running_backend; then
    echo "$APP_NAME_BACKEND 已在运行，PID: $(cat "$BACKEND_PID_FILE")"
    return 0
  fi

  # 检查并清理端口
  kill_port "$SERVER_PORT_VALUE" "$APP_NAME_BACKEND"

  ensure_dirs

  echo "启动 $APP_NAME_BACKEND..."
  echo "  - 端口: $SERVER_PORT_VALUE"
  echo "  - 地址: $SERVER_ADDRESS_VALUE"
  echo "  - 数据库用户: $DB_USER_VALUE"
  (
    export DB_USER="$DB_USER_VALUE"
    export DB_PASSWORD="$DB_PASSWORD_VALUE"
    export SERVER_ADDRESS="$SERVER_ADDRESS_VALUE"
    export SERVER_PORT="$SERVER_PORT_VALUE"
    if [[ -n "$SPRING_PROFILE_VALUE" ]]; then
      export SPRING_PROFILES_ACTIVE="$SPRING_PROFILE_VALUE"
    fi

    nohup "${MVN_CMD[@]}" > "$BACKEND_LOG_FILE" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
  )

  sleep 3
  if is_running_backend && wait_for_backend; then
    echo "$APP_NAME_BACKEND 启动成功，PID: $(cat "$BACKEND_PID_FILE")"
    echo "访问地址：http://localhost:$SERVER_PORT_VALUE"
    echo "Swagger文档：http://localhost:$SERVER_PORT_VALUE/swagger-ui.html"
    echo "日志：$BACKEND_LOG_FILE"
    return 0
  fi

  echo "$APP_NAME_BACKEND 启动失败，请查看日志：$BACKEND_LOG_FILE"
  tail -n 120 "$BACKEND_LOG_FILE" || true
  return 1
}

start_frontend() {
  if is_running_frontend; then
    echo "$APP_NAME_FRONTEND 已在运行，PID: $(cat "$FRONTEND_PID_FILE")"
    return 0
  fi

  # 检查并清理端口
  kill_port "$FRONTEND_PORT_VALUE" "$APP_NAME_FRONTEND"

  ensure_dirs

  echo "启动 $APP_NAME_FRONTEND..."
  echo "  - 端口: $FRONTEND_PORT_VALUE"
  echo "  - 地址: $FRONTEND_HOST_VALUE"
  (
    nohup "${NPM_CMD[@]}" > "$FRONTEND_LOG_FILE" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"
  )

  sleep 3
  if is_running_frontend; then
    echo "$APP_NAME_FRONTEND 启动成功，PID: $(cat "$FRONTEND_PID_FILE")"
    echo "访问地址：http://localhost:$FRONTEND_PORT_VALUE"
    echo "日志：$FRONTEND_LOG_FILE"
  else
    echo "$APP_NAME_FRONTEND 启动失败，请查看日志：$FRONTEND_LOG_FILE"
    return 1
  fi
}

start() {
  start_backend
  start_frontend
}

start_backend_only() {
  start_backend
}

start_frontend_only() {
  start_frontend
}

stop_backend() {
  if ! is_running_backend; then
    echo "$APP_NAME_BACKEND 未运行"
    # 即使进程不在运行，也尝试清理端口
    kill_port "$SERVER_PORT_VALUE" "$APP_NAME_BACKEND" || true
    return 0
  fi

  local pid
  pid="$(cat "$BACKEND_PID_FILE")"
  echo "停止 $APP_NAME_BACKEND (PID: $pid)..."
  kill "$pid" 2>/dev/null || true

  for _ in {1..10}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$BACKEND_PID_FILE"
      echo "$APP_NAME_BACKEND 已停止"
      # 确保端口被释放
      kill_port "$SERVER_PORT_VALUE" "$APP_NAME_BACKEND" || true
      return 0
    fi
    sleep 1
  done

  echo "进程未退出，尝试强制终止..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$BACKEND_PID_FILE"
  sleep 1
  # 确保端口被释放
  kill_port "$SERVER_PORT_VALUE" "$APP_NAME_BACKEND" || true
  echo "$APP_NAME_BACKEND 已强制停止"
}

stop_frontend() {
  if ! is_running_frontend; then
    echo "$APP_NAME_FRONTEND 未运行"
    # 即使进程不在运行，也尝试清理端口
    kill_port "$FRONTEND_PORT_VALUE" "$APP_NAME_FRONTEND" || true
    return 0
  fi

  local pid
  pid="$(cat "$FRONTEND_PID_FILE")"
  echo "停止 $APP_NAME_FRONTEND (PID: $pid)..."
  kill "$pid" 2>/dev/null || true

  for _ in {1..10}; do
    if ! kill -0 "$pid" 2>/dev/null; then
      rm -f "$FRONTEND_PID_FILE"
      echo "$APP_NAME_FRONTEND 已停止"
      # 确保端口被释放
      kill_port "$FRONTEND_PORT_VALUE" "$APP_NAME_FRONTEND" || true
      return 0
    fi
    sleep 1
  done

  echo "进程未退出，尝试强制终止..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$FRONTEND_PID_FILE"
  sleep 1
  # 确保端口被释放
  kill_port "$FRONTEND_PORT_VALUE" "$APP_NAME_FRONTEND" || true
  echo "$APP_NAME_FRONTEND 已强制停止"
}

stop() {
  stop_frontend
  stop_backend
}

restart() {
  echo "=========================================="
  echo "重启服务..."
  echo "=========================================="
  stop
  echo ""
  echo "等待3秒后启动服务..."
  sleep 3
  echo ""
  start
}

restart_backend_only() {
  echo "=========================================="
  echo "重启后端服务..."
  echo "=========================================="
  stop_backend
  echo ""
  echo "等待2秒后启动后端..."
  sleep 2
  echo ""
  start_backend
}

restart_frontend_only() {
  echo "=========================================="
  echo "重启前端服务..."
  echo "=========================================="
  stop_frontend
  echo ""
  echo "等待2秒后启动前端..."
  sleep 2
  echo ""
  start_frontend
}

status() {
  echo "=========================================="
  echo "服务状态"
  echo "=========================================="
  if is_running_backend; then
    echo "✓ $APP_NAME_BACKEND 运行中"
    echo "  PID: $(cat "$BACKEND_PID_FILE")"
    echo "  端口: $SERVER_PORT_VALUE"
    echo "  访问: http://localhost:$SERVER_PORT_VALUE"
  else
    echo "✗ $APP_NAME_BACKEND 未运行"
  fi
  echo ""
  if is_running_frontend; then
    echo "✓ $APP_NAME_FRONTEND 运行中"
    echo "  PID: $(cat "$FRONTEND_PID_FILE")"
    echo "  端口: $FRONTEND_PORT_VALUE"
    echo "  访问: http://localhost:$FRONTEND_PORT_VALUE"
  else
    echo "✗ $APP_NAME_FRONTEND 未运行"
  fi
  echo "=========================================="
}

logs() {
  local target="${2:-backend}"
  if [[ "$target" == "frontend" ]]; then
    if [[ ! -f "$FRONTEND_LOG_FILE" ]]; then
      echo "日志不存在：$FRONTEND_LOG_FILE"
      return 1
    fi
    tail -n 200 -f "$FRONTEND_LOG_FILE"
    return 0
  fi
  if [[ ! -f "$BACKEND_LOG_FILE" ]]; then
    echo "日志不存在：$BACKEND_LOG_FILE"
    return 1
  fi
  tail -n 200 -f "$BACKEND_LOG_FILE"
}

usage() {
  cat <<USAGE
========================================
NPdatabase 服务管理脚本
========================================

用法：$(basename "$0") {start|stop|restart|status|logs [backend|frontend]|start-backend|start-frontend|restart-backend|restart-frontend}

命令说明：
  start    - 启动前后端服务
  stop     - 停止前后端服务
  restart  - 重启前后端服务
  status   - 查看服务运行状态
  logs     - 查看日志（默认后端，可指定 frontend）
  start-backend   - 仅启动后端服务
  start-frontend  - 仅启动前端服务
  restart-backend - 仅重启后端服务
  restart-frontend- 仅重启前端服务

固定端口配置：
  后端端口: $SERVER_PORT_VALUE
  前端端口: $FRONTEND_PORT_VALUE

可选环境变量（高级用户）：
  DB_USER                 数据库用户（默认：yfguo）
  DB_PASSWORD             数据库密码（默认：npdb2024）
  SERVER_ADDRESS          后端绑定地址（默认：0.0.0.0）
  SERVER_PORT             后端端口（默认：8080）
  FRONTEND_HOST           前端绑定地址（默认：0.0.0.0）
  FRONTEND_PORT           前端端口（默认：3001）

示例：
  $(basename "$0") start          # 启动服务
  $(basename "$0") stop           # 停止服务
  $(basename "$0") restart        # 重启服务
  $(basename "$0") status         # 查看状态
  $(basename "$0") logs           # 查看后端日志
  $(basename "$0") logs frontend  # 查看前端日志
  $(basename "$0") start-backend  # 仅启动后端
  $(basename "$0") restart-backend# 仅重启后端

========================================
USAGE
}

case "${1:-}" in
  start) start ;;
  start-backend) start_backend_only ;;
  start-frontend) start_frontend_only ;;
  stop) stop ;;
  restart) restart ;;
  restart-backend) restart_backend_only ;;
  restart-frontend) restart_frontend_only ;;
  status) status ;;
  logs) logs "$@" ;;
  *) usage ; exit 1 ;;
esac
