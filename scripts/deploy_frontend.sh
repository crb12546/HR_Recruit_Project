#!/bin/bash
# 前端部署脚本

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

echo "开始部署前端应用到 $DEPLOY_ENV 环境..."

# 项目根目录
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FRONTEND_DIR="$PROJECT_ROOT/frontend"

# 切换到前端目录
cd "$FRONTEND_DIR"

# 创建环境配置文件
create_env_file() {
    echo "创建 $DEPLOY_ENV 环境配置文件..."
    
    # 根据环境创建不同的配置
    if [ "$DEPLOY_ENV" = "production" ]; then
        cat > .env.production << EOL
NODE_ENV=production
VUE_APP_API_BASE_URL=https://api.hr-recruitment.example.com/api/v1
VUE_APP_TITLE=HR招聘系统
VUE_APP_OSS_BUCKET=${ALIYUN_OSS_BUCKET:-hr-recruitment-files}
VUE_APP_OSS_REGION=${ALIYUN_REGION_ID:-cn-shanghai}
EOL
    elif [ "$DEPLOY_ENV" = "testing" ]; then
        cat > .env.testing << EOL
NODE_ENV=testing
VUE_APP_API_BASE_URL=http://test-api.hr-recruitment.example.com/api/v1
VUE_APP_TITLE=HR招聘系统(测试)
VUE_APP_OSS_BUCKET=${ALIYUN_OSS_BUCKET:-hr-recruitment-files-test}
VUE_APP_OSS_REGION=${ALIYUN_REGION_ID:-cn-shanghai}
EOL
    else
        cat > .env.development << EOL
NODE_ENV=development
VUE_APP_API_BASE_URL=http://localhost:8000/api/v1
VUE_APP_TITLE=HR招聘系统(开发)
VUE_APP_OSS_BUCKET=${ALIYUN_OSS_BUCKET:-hr-recruitment-files-dev}
VUE_APP_OSS_REGION=${ALIYUN_REGION_ID:-cn-shanghai}
EOL
    fi
    
    echo "环境配置文件创建完成"
}

# 安装依赖
install_dependencies() {
    echo "安装依赖..."
    npm install
}

# 构建应用
build_application() {
    echo "构建应用..."
    if [ "$DEPLOY_ENV" = "production" ]; then
        npm run build
    elif [ "$DEPLOY_ENV" = "testing" ]; then
        npm run build:test
    else
        npm run build:dev
    fi
}

# 部署到阿里云OSS
deploy_to_oss() {
    echo "部署到阿里云OSS..."
    
    # 检查是否安装了ossutil
    if ! command -v ossutil > /dev/null; then
        echo "错误: 未安装ossutil工具，请先安装"
        echo "安装指南: https://help.aliyun.com/document_detail/120075.html"
        exit 1
    fi
    
    # 检查环境变量
    if [ -z "$ALIYUN_ACCESS_KEY" ] || [ -z "$ALIYUN_ACCESS_SECRET" ]; then
        echo "错误: 缺少阿里云访问密钥环境变量"
        echo "请设置 ALIYUN_ACCESS_KEY 和 ALIYUN_ACCESS_SECRET 环境变量"
        exit 1
    fi
    
    # 配置ossutil
    ossutil config -e oss-${ALIYUN_REGION_ID:-cn-shanghai}.aliyuncs.com -i $ALIYUN_ACCESS_KEY -k $ALIYUN_ACCESS_SECRET
    
    # 上传文件
    BUCKET_NAME=${ALIYUN_OSS_BUCKET:-hr-recruitment-files}
    if [ "$DEPLOY_ENV" = "testing" ]; then
        BUCKET_NAME=${ALIYUN_OSS_BUCKET:-hr-recruitment-files-test}
    elif [ "$DEPLOY_ENV" = "development" ]; then
        BUCKET_NAME=${ALIYUN_OSS_BUCKET:-hr-recruitment-files-dev}
    fi
    
    echo "上传到存储桶: $BUCKET_NAME"
    ossutil cp -r dist/ oss://$BUCKET_NAME/ --update
    
    echo "部署完成! 访问地址: https://$BUCKET_NAME.oss-${ALIYUN_REGION_ID:-cn-shanghai}.aliyuncs.com/index.html"
}

# 主函数
main() {
    echo "开始部署流程..."
    create_env_file
    install_dependencies
    build_application
    
    # 如果是生产或测试环境，部署到OSS
    if [ "$DEPLOY_ENV" = "production" ] || [ "$DEPLOY_ENV" = "testing" ]; then
        deploy_to_oss
    else
        echo "开发环境构建完成，跳过部署到OSS"
    fi
    
    echo "部署完成!"
}

# 执行主函数
main
