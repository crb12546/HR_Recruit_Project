"""开发环境配置"""
from typing import Dict, Any

# 开发环境配置
DEVELOPMENT_CONFIG: Dict[str, Any] = {
    "TESTING": False,
    "DEBUG": True,
    "DATABASE_URL": "mysql+mysqlconnector://root:password@localhost:3306/hr_recruit_dev",
    "MOCK_SERVICES": False,
    "OCR_SERVICE": "aliyun",
    "STORAGE_SERVICE": "aliyun",
    "GPT_SERVICE": "openai",
    "ALIYUN_ACCESS_KEY": "",
    "ALIYUN_SECRET_KEY": "",
    "ALIYUN_REGION": "cn-hangzhou",
    "ALIYUN_BUCKET": "hr-recruit-dev",
    "OPENAI_API_KEY": ""
}

def get_development_config() -> Dict[str, Any]:
    """获取开发环境配置"""
    return DEVELOPMENT_CONFIG
