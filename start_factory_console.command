#!/bin/zsh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$ROOT_DIR/backend"
FRONTEND_DIR="$ROOT_DIR/frontend"
RUNTIME_DIR="$ROOT_DIR/runtime"
LOG_DIR="$RUNTIME_DIR/logs"
PID_DIR="$RUNTIME_DIR/pids"

mkdir -p "$LOG_DIR" "$PID_DIR"

BACKEND_PID_FILE="$PID_DIR/backend.pid"
FRONTEND_PID_FILE="$PID_DIR/frontend.pid"

if [[ -x "$BACKEND_DIR/.venv/bin/python" ]]; then
  PYTHON_BIN="$BACKEND_DIR/.venv/bin/python"
else
  PYTHON_BIN="python3"
fi

if [[ ! -d "$FRONTEND_DIR/node_modules" ]]; then
  echo "缺少前端依赖，请先双击 install_factory_console.command 完成安装。"
  exit 1
fi

if [[ ! -f "$FRONTEND_DIR/.next/BUILD_ID" ]]; then
  echo "正在构建前端，请稍候..."
  cd "$FRONTEND_DIR"
  npm run build
fi

start_if_needed() {
  local pid_file="$1"
  local command="$2"
  local log_file="$3"

  if [[ -f "$pid_file" ]]; then
    local existing_pid
    existing_pid="$(cat "$pid_file")"
    if kill -0 "$existing_pid" >/dev/null 2>&1; then
      return 0
    fi
    rm -f "$pid_file"
  fi

  nohup /bin/bash -lc "$command" >"$log_file" 2>&1 &
  echo $! >"$pid_file"
}

start_if_needed \
  "$BACKEND_PID_FILE" \
  "cd '$BACKEND_DIR' && '$PYTHON_BIN' -m uvicorn app.main:app --host 127.0.0.1 --port 8001" \
  "$LOG_DIR/backend.log"

start_if_needed \
  "$FRONTEND_PID_FILE" \
  "cd '$FRONTEND_DIR' && NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8001 npm run start -- --hostname 127.0.0.1 --port 3001" \
  "$LOG_DIR/frontend.log"

echo "工厂 AI 视频工厂已启动。"
echo "前端地址: http://127.0.0.1:3001"
echo "后端地址: http://127.0.0.1:8001"
echo "日志目录: $LOG_DIR"
