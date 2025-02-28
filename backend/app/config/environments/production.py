"""生产环境配置"""
from typing import Dict, Any

# 生产环境配置
PRODUCTION_CONFIG: Dict[str, Any] = {
    "TESTING": False,
    "DEBUG": False,
    "DATABASE_URL": "mysql+mysqlconnector://root:password@localhost:3306/hr_recruit",
    "MOCK_SERVICES": False,
    "OCR_SERVICE": "aliyun",
    "STORAGE_SERVICE": "aliyun",
    "GPT_SERVICE": "openai",
    "ALIYUN_ACCESS_KEY": "",
    "ALIYUN_SECRET_KEY": "",
    "ALIYUN_REGION": "cn-hangzhou",
    "ALIYUN_BUCKET": "hr-recruit",
    "OPENAI_API_KEY": ""
}

def get_production_config() -> Dict[str, Any]:
    """获取生产环境配置"""
    return PRODUCTION_CONFIG
