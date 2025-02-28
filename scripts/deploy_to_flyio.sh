#!/bin/bash
# fly.io部署脚本

set -e

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -b, --backend       部署后端"
    echo "  -f, --frontend      部署前端"
    echo "  -a, --all           部署前端和后端"
    echo "  -h, --help          显示帮助信息"
    exit 0
}

# 默认不部署任何服务
DEPLOY_BACKEND=false
DEPLOY_FRONTEND=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -b|--backend)
            DEPLOY_BACKEND=true
            shift
            ;;
        -f|--frontend)
            DEPLOY_FRONTEND=true
            shift
            ;;
        -a|--all)
            DEPLOY_BACKEND=true
            DEPLOY_FRONTEND=true
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

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# 部署后端
deploy_backend() {
    echo "开始部署后端..."
    cd "$PROJECT_ROOT/backend"
    
    # 检查fly.toml是否存在
    if [ ! -f "fly.toml" ]; then
        echo "错误: 找不到fly.toml配置文件"
        exit 1
    fi
    
    # 部署到fly.io
    echo "部署到fly.io..."
    $FLYCTL_INSTALL/bin/flyctl deploy --remote-only
    
    echo "后端部署完成!"
}

# 部署前端
deploy_frontend() {
    echo "开始部署前端..."
    cd "$PROJECT_ROOT/frontend"
    
    # 检查fly.toml是否存在
    if [ ! -f "fly.toml" ]; then
        echo "错误: 找不到fly.toml配置文件"
        exit 1
    fi
    
    # 部署到fly.io
    echo "部署到fly.io..."
    $FLYCTL_INSTALL/bin/flyctl deploy --remote-only
    
    echo "前端部署完成!"
}

# 主函数
main() {
    echo "开始部署流程..."
    
    if [ "$DEPLOY_BACKEND" = true ]; then
        deploy_backend
    fi
    
    if [ "$DEPLOY_FRONTEND" = true ]; then
        deploy_frontend
    fi
    
    if [ "$DEPLOY_BACKEND" = false ] && [ "$DEPLOY_FRONTEND" = false ]; then
        echo "错误: 请指定要部署的服务 (-b, -f 或 -a)"
        show_help
    fi
    
    echo "部署完成!"
}

# 执行主函数
main
