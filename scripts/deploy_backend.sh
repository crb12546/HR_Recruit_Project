#!/bin/bash
# 后端部署脚本

set -e

# 显示帮助信息
show_help() {
    echo "用法: $0 [选项]"
    echo "选项:"
    echo "  -e, --env ENV       指定部署环境 (development, testing, production)"
    echo "  -h, --help          显示帮助信息"
    exit 0
}

# 默认环境
DEPLOY_ENV="production"

# 解析命令行参数
while [[ $# -gt 0 ]]; do
    key="$1"
    case $key in
        -e|--env)
            DEPLOY_ENV="$2"
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

echo "开始部署后端应用到 $DEPLOY_ENV 环境..."

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
BACKEND_DIR="$PROJECT_ROOT/backend"

# 切换到后端目录
cd "$BACKEND_DIR"

# 加载环境变量
if [ -f ".env.$DEPLOY_ENV" ]; then
    echo "加载 $DEPLOY_ENV 环境配置..."
    set -a
    source ".env.$DEPLOY_ENV"
    set +a
else
    echo "错误: 找不到环境配置文件 .env.$DEPLOY_ENV"
    exit 1
fi

# 检查必要的环境变量
check_env_vars() {
    local missing_vars=()
    
    if [ "$DEPLOY_ENV" = "production" ]; then
        # 生产环境必需的变量
        for var in DB_PASSWORD ALIYUN_ACCESS_KEY ALIYUN_ACCESS_SECRET GPT_API_KEY; do
            if [ -z "${!var}" ]; then
                missing_vars+=("$var")
            fi
        done
    fi
    
    if [ ${#missing_vars[@]} -gt 0 ]; then
        echo "错误: 缺少以下必要的环境变量:"
        for var in "${missing_vars[@]}"; do
            echo "  - $var"
        done
        exit 1
    fi
}

# 安装依赖
install_dependencies() {
    echo "安装依赖..."
    pip install -r requirements.txt
}

# 初始化数据库
init_database() {
    echo "初始化数据库..."
    if [ "$DEPLOY_ENV" = "production" ]; then
        # 生产环境使用MySQL
        echo "创建数据库表..."
        python -c "from app.models.all_models import *; from app.database import engine; Base.metadata.create_all(bind=engine)"
    else
        # 开发和测试环境
        echo "使用开发/测试数据库..."
        python -c "from app.models.all_models import *; from app.database import engine; Base.metadata.create_all(bind=engine)"
    fi
}

# 启动应用
start_application() {
    echo "启动应用..."
    if [ "$DEPLOY_ENV" = "production" ]; then
        # 生产环境使用gunicorn
        echo "使用gunicorn启动应用..."
        gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000 --daemon
    else
        # 开发和测试环境使用uvicorn
        echo "使用uvicorn启动应用..."
        uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
    fi
}

# 主函数
main() {
    echo "开始部署流程..."
    check_env_vars
    install_dependencies
    init_database
    start_application
    echo "部署完成!"
}

# 执行主函数
main
