"""验证服务配置"""
import os
import sys
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent.parent
sys.path.append(str(backend_dir))

from app.database import get_db
from app.services.mock_gpt import MockGPTService
from app.services.mock_ocr import MockOCRService
from app.services.mock_storage import MockStorageService
from app.services.mock_tag import MockTagService

def verify_services():
    """验证所有服务配置"""
    print("开始验证服务配置...")
    
    # 验证数据库连接
    try:
        db = next(get_db())
        print("✓ 数据库连接成功")
    except Exception as e:
        print(f"✗ 数据库连接失败: {str(e)}")
        raise
        
    # 验证模拟服务
    try:
        gpt = MockGPTService()
        ocr = MockOCRService()
        storage = MockStorageService()
        tag = MockTagService()
        print("✓ 所有模拟服务导入成功")
    except Exception as e:
        print(f"✗ 模拟服务导入失败: {str(e)}")
        raise
        
    # 验证环境变量
    required_vars = [
        "ENV",
        "MOCK_SERVICES",
        "OPENAI_API_KEY",
        "ALIYUN_ACCESS_KEY_ID",
        "ALIYUN_ACCESS_KEY_SECRET",
        "ALIYUN_OSS_BUCKET",
        "ALIYUN_OSS_ENDPOINT",
        "ALIYUN_REGION"
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
            
    if missing_vars:
        print(f"✗ 缺少必要的环境变量: {', '.join(missing_vars)}")
    else:
        print("✓ 所有必要的环境变量已设置")
        
    print("\n环境变量值:")
    for var in required_vars:
        value = os.getenv(var, "未设置")
        if any(key in var.lower() for key in ["key", "secret", "password"]):
            value = value[:8] + "..." if value != "未设置" else value
        print(f"{var}: {value}")

if __name__ == "__main__":
    verify_services()
