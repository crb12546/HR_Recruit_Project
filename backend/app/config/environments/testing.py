"""测试环境配置"""
from typing import Dict, Any

# 测试环境配置
TESTING_CONFIG: Dict[str, Any] = {
    "TESTING": True,
    "DEBUG": True,
    "DATABASE_URL": "mysql+mysqlconnector://testuser:testpassword@db:3306/hr_recruit_test",
    "MOCK_SERVICES": True,
    "OCR_SERVICE": "mock",
    "STORAGE_SERVICE": "mock",
    "GPT_SERVICE": "mock",
    "ALIYUN_ACCESS_KEY": "",
    "ALIYUN_SECRET_KEY": "",
    "ALIYUN_REGION": "cn-hangzhou",
    "ALIYUN_BUCKET": "hr-recruit-test",
    "OPENAI_API_KEY": ""
}

def get_testing_config() -> Dict[str, Any]:
    """获取测试环境配置"""
    return TESTING_CONFIG
