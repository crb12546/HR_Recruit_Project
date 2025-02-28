#!/bin/bash
# 初始化日志目录脚本

set -e

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"
LOGS_DIR="$BACKEND_DIR/logs"

# 创建日志目录
echo "创建日志目录: $LOGS_DIR"
mkdir -p "$LOGS_DIR"

# 设置权限
echo "设置日志目录权限..."
chmod 755 "$LOGS_DIR"

# 创建日志文件
echo "创建日志文件..."
touch "$LOGS_DIR/app.log"
touch "$LOGS_DIR/error.log"
touch "$LOGS_DIR/access.log"

# 设置日志文件权限
echo "设置日志文件权限..."
chmod 644 "$LOGS_DIR/app.log"
chmod 644 "$LOGS_DIR/error.log"
chmod 644 "$LOGS_DIR/access.log"

echo "日志目录初始化完成!"
