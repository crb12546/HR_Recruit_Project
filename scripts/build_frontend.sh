#!/bin/bash
# 前端构建脚本

set -e

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -e, --env ENV       指定构建环境 (development, testing, production)"
    echo "  -h, --help          显示帮助信息"
    exit 0
}

# 默认环境
BUILD_ENV="production"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -e|--env)
            BUILD_ENV="$2"
            shift
            shift
            ;;
        -h|--help)
            show_help
            ;;
        *)
            echo "未知选项: $1"
            show_help
            ;;
    esac
done

echo "开始构建前端应用 ($BUILD_ENV 环境)..."

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 切换到前端目录
cd "$FRONTEND_DIR"

# 安装依赖
echo "安装依赖..."
npm install

# 构建应用
echo "构建应用..."
if [ "$BUILD_ENV" = "production" ]; then
    npm run build
elif [ "$BUILD_ENV" = "testing" ]; then
    npm run build:test
else
    npm run build:dev
fi

echo "构建完成! 输出目录: $FRONTEND_DIR/dist"
