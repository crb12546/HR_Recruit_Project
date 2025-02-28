#!/bin/bash

# 设置默认参数
BUILD=true
CLEAN=true
TESTS="all"
REGENERATE_DATA=false

# 解析命令行参数
while [[ $# -gt 0 ]]; do
  case $1 in
    --no-build)
      BUILD=false
      shift
      ;;
    --no-clean)
      CLEAN=false
      shift
      ;;
    --tests=*)
      TESTS="${1#*=}"
      shift
      ;;
    --regenerate-data)
      REGENERATE_DATA=true
      shift
      ;;
    *)
      echo "未知参数: $1"
      exit 1
      ;;
  esac
done

# 设置环境变量
export TESTING=True
export MOCK_SERVICES=True

# 初始化模拟数据
echo "初始化模拟数据..."
if [ "$REGENERATE_DATA" = true ]; then
  python backend/tests/mocks/init_mock_data.py --regenerate
else
  python backend/tests/mocks/init_mock_data.py
fi

# 构建测试容器
if [ "$BUILD" = true ]; then
  echo "构建测试容器..."
  docker-compose -f docker-compose.test.yml build
fi

# 根据测试类型运行不同的测试命令
if [ "$TESTS" = "all" ]; then
  TEST_CMD="pytest -xvs tests/"
elif [ "$TESTS" = "unit" ]; then
  TEST_CMD="pytest -xvs tests/unit/"
elif [ "$TESTS" = "integration" ]; then
  TEST_CMD="pytest -xvs tests/integration/"
elif [ "$TESTS" = "e2e" ]; then
  TEST_CMD="pytest -xvs tests/e2e/"
elif [ "$TESTS" = "standalone" ]; then
  TEST_CMD="pytest -xvs tests/standalone/"
else
  TEST_CMD="pytest -xvs $TESTS"
fi

# 更新docker-compose命令
sed -i "s|pytest -xvs tests/|$TEST_CMD|g" docker-compose.test.yml

echo "启动测试容器..."
docker-compose -f docker-compose.test.yml up

# 清理测试容器
if [ "$CLEAN" = true ]; then
  echo "清理测试容器..."
  docker-compose -f docker-compose.test.yml down -v
fi

echo "测试完成"

# 恢复docker-compose文件
sed -i "s|$TEST_CMD|pytest -xvs tests/|g" docker-compose.test.yml
