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
SERVER_ADDRESS_VALUE="${SERVER_ADDRESS:-}"
SERVER_PORT_VALUE="${SERVER_PORT:-}"
FRONTEND_HOST_VALUE="${FRONTEND_HOST:-127.0.0.1}"
FRONTEND_PORT_VALUE="${FRONTEND_PORT:-5173}"

MVN_CMD=(mvn -f "$ROOT_DIR/backend/pom.xml" spring-boot:run -DskipTests)
NPM_CMD=(npm --prefix "$FRONTEND_DIR" run dev -- --host "$FRONTEND_HOST_VALUE" --port "$FRONTEND_PORT_VALUE")

ensure_dirs() {
  mkdir -p "$(dirname "$BACKEND_PID_FILE")" "$(dirname "$BACKEND_LOG_FILE")"
  mkdir -p "$(dirname "$FRONTEND_PID_FILE")" "$(dirname "$FRONTEND_LOG_FILE")"
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

  ensure_dirs

  echo "启动 $APP_NAME_BACKEND..."
  (
    export DB_USER="$DB_USER_VALUE"
    export DB_PASSWORD="$DB_PASSWORD_VALUE"
    if [[ -n "$SPRING_PROFILE_VALUE" ]]; then
      export SPRING_PROFILES_ACTIVE="$SPRING_PROFILE_VALUE"
    fi
    if [[ -n "$SERVER_ADDRESS_VALUE" ]]; then
      export SERVER_ADDRESS="$SERVER_ADDRESS_VALUE"
    fi
    if [[ -n "$SERVER_PORT_VALUE" ]]; then
      export SERVER_PORT="$SERVER_PORT_VALUE"
    fi

    nohup "${MVN_CMD[@]}" > "$BACKEND_LOG_FILE" 2>&1 &
    echo $! > "$BACKEND_PID_FILE"
  )

  sleep 1
  if is_running_backend; then
    echo "$APP_NAME_BACKEND 启动成功，PID: $(cat "$BACKEND_PID_FILE")"
    echo "日志：$BACKEND_LOG_FILE"
  else
    echo "$APP_NAME_BACKEND 启动失败，请查看日志：$BACKEND_LOG_FILE"
    return 1
  fi
}

start_frontend() {
  if is_running_frontend; then
    echo "$APP_NAME_FRONTEND 已在运行，PID: $(cat "$FRONTEND_PID_FILE")"
    return 0
  fi

  ensure_dirs

  echo "启动 $APP_NAME_FRONTEND..."
  (
    nohup "${NPM_CMD[@]}" > "$FRONTEND_LOG_FILE" 2>&1 &
    echo $! > "$FRONTEND_PID_FILE"
  )

  sleep 1
  if is_running_frontend; then
    echo "$APP_NAME_FRONTEND 启动成功，PID: $(cat "$FRONTEND_PID_FILE")"
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

stop_backend() {
  if ! is_running_backend; then
    echo "$APP_NAME_BACKEND 未运行"
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
      return 0
    fi
    sleep 1
  done

  echo "进程未退出，尝试强制终止..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$BACKEND_PID_FILE"
  echo "$APP_NAME_BACKEND 已强制停止"
}

stop_frontend() {
  if ! is_running_frontend; then
    echo "$APP_NAME_FRONTEND 未运行"
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
      return 0
    fi
    sleep 1
  done

  echo "进程未退出，尝试强制终止..."
  kill -9 "$pid" 2>/dev/null || true
  rm -f "$FRONTEND_PID_FILE"
  echo "$APP_NAME_FRONTEND 已强制停止"
}

stop() {
  stop_frontend
  stop_backend
}

restart() {
  stop
  start
}

status() {
  if is_running_backend; then
    echo "$APP_NAME_BACKEND 运行中，PID: $(cat "$BACKEND_PID_FILE")"
  else
    echo "$APP_NAME_BACKEND 未运行"
  fi
  if is_running_frontend; then
    echo "$APP_NAME_FRONTEND 运行中，PID: $(cat "$FRONTEND_PID_FILE")"
  else
    echo "$APP_NAME_FRONTEND 未运行"
  fi
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
用法：$(basename "$0") {start|stop|restart|status|logs [backend|frontend]}

可选环境变量：
  DB_USER                 数据库用户（默认：postgres）
  DB_PASSWORD             数据库密码（默认：空）
  SPRING_PROFILES_ACTIVE  Spring Profile
  SERVER_ADDRESS          绑定地址（默认：空，建议 0.0.0.0）
  SERVER_PORT             端口（默认：8080）
  FRONTEND_HOST           前端绑定地址（默认：0.0.0.0）
  FRONTEND_PORT           前端端口（默认：5173）
USAGE
}

case "${1:-}" in
  start) start ;;
  stop) stop ;;
  restart) restart ;;
  status) status ;;
  logs) logs "$@" ;;
  *) usage ; exit 1 ;;
esac
