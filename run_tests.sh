#!/bin/bash

# 设置环境变量
export TESTING=True
export MOCK_SERVICES=True

# 初始化模拟数据
echo "初始化模拟数据..."
python backend/tests/mocks/init_mock_data.py

# 构建并启动测试容器
echo "构建测试容器..."
docker-compose -f docker-compose.test.yml build

echo "启动测试容器..."
docker-compose -f docker-compose.test.yml up

# 清理测试容器
echo "清理测试容器..."
docker-compose -f docker-compose.test.yml down -v

echo "测试完成"
