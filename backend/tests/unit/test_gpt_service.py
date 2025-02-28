"""GPT服务单元测试"""
import pytest
from unittest.mock import MagicMock, patch
from app.services.gpt import GPTService, OpenAIGPTService, MockGPTService

class TestGPTService:
    """GPT服务测试类"""
    
    def test_openai_gpt_service(self, monkeypatch):
        """测试OpenAI GPT服务"""
        # 模拟OpenAI客户端
        mock_client = MagicMock()
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "GPT生成的内容"
        mock_client.chat.completions.create.return_value = mock_response
        
        # 打补丁替换OpenAI客户端
        monkeypatch.setattr("app.services.gpt.OpenAI", lambda api_key: mock_client)
        
        # 创建GPT服务
        gpt_service = OpenAIGPTService(api_key="test_key")
        
        # 调用解析简历方法
        result = gpt_service.parse_resume("简历文本内容")
        
        # 验证结果
        assert result == "GPT生成的内容"
        assert mock_client.chat.completions.create.called
        
        # 调用生成人才画像方法
        result = gpt_service.generate_talent_portrait("解析后的简历内容")
        
        # 验证结果
        assert result == "GPT生成的内容"
        assert mock_client.chat.completions.create.call_count == 2
    
    def test_mock_gpt_service(self):
        """测试模拟GPT服务"""
        # 创建模拟GPT服务
        gpt_service = MockGPTService()
        
        # 调用解析简历方法
        result = gpt_service.parse_resume("简历文本内容")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        
        # 调用生成人才画像方法
        result = gpt_service.generate_talent_portrait("解析后的简历内容")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, str)
        assert len(result) > 0
        
        # 调用生成面试问题方法
        result = gpt_service.generate_interview_questions("职位描述", "简历内容")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, list)
        assert len(result) > 0
        
        # 调用匹配职位方法
        result = gpt_service.match_job_requirements("职位描述", "简历内容")
        
        # 验证结果
        assert result is not None
        assert isinstance(result, dict)
        assert "score" in result
        assert "analysis" in result
    
    def test_gpt_service_factory(self, monkeypatch):
        """测试GPT服务工厂"""
        from app.services.service_factory import get_gpt_service
        
        # 模拟配置
        mock_config = {
            "GPT_SERVICE": "mock",
            "OPENAI_API_KEY": "test_key"
        }
        
        # 打补丁替换配置
        monkeypatch.setattr("app.services.service_factory.get_config", lambda: mock_config)
        
        # 获取GPT服务
        gpt_service = get_gpt_service()
        
        # 验证结果
        assert gpt_service is not None
        assert isinstance(gpt_service, GPTService)
        assert isinstance(gpt_service, MockGPTService)
        
        # 修改配置为OpenAI
        mock_config["GPT_SERVICE"] = "openai"
        
        # 获取GPT服务
        gpt_service = get_gpt_service()
        
        # 验证结果
        assert gpt_service is not None
        assert isinstance(gpt_service, GPTService)
        assert isinstance(gpt_service, OpenAIGPTService)
