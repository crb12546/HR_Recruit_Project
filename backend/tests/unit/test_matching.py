"""简历匹配服务测试"""
import pytest
from app.services.matching import MatchingService, MatchResult
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.tag import Tag

def test_match_result_creation():
    """测试匹配结果创建"""
    result = MatchResult(
        score=85.5,
        details={
            "技能匹配": 90,
            "经验要求": 85,
            "教育背景": 80
        },
        recommendations=[
            "建议强化项目管理经验",
            "可以补充相关认证"
        ]
    )
    
    assert result.score == 85.5
    assert result.details["技能匹配"] == 90
    assert len(result.recommendations) == 2

def test_calculate_match(db_session):
    """测试简历匹配计算"""
    # 创建测试数据
    resume = Resume(
        candidate_name="张三",
        file_url="test_url",
        file_type="pdf",
        ocr_content="5年Python开发经验，精通FastAPI",
        talent_portrait="资深后端开发工程师"
    )
    resume.tags = [
        Tag(name="Python", category="技能"),
        Tag(name="FastAPI", category="技能"),
        Tag(name="5年", category="经验")
    ]
    
    job = JobRequirement(
        position_name="高级Python工程师",
        department="技术部",
        responsibilities="负责后端服务开发",
        requirements="精通Python，熟悉FastAPI，5年以上经验",
        salary_range="25k-35k",
        location="北京"
    )
    
    # 初始化服务
    matching_service = MatchingService()
    
    # 计算匹配度
    result = matching_service.calculate_match(resume, job)
    
    # 验证结果
    assert isinstance(result, MatchResult)
    assert 0 <= result.score <= 100
    assert "技能匹配" in result.details
    assert len(result.recommendations) > 0

def test_rank_resumes(db_session):
    """测试简历排序"""
    # 创建测试数据
    resumes = [
        Resume(
            candidate_name="张三",
            file_url="test_url_1",
            file_type="pdf",
            ocr_content="5年Python开发经验",
            talent_portrait="资深工程师",
            tags=[Tag(name="Python", category="技能")]
        ),
        Resume(
            candidate_name="李四",
            file_url="test_url_2",
            file_type="pdf",
            ocr_content="3年Java开发经验",
            talent_portrait="中级工程师",
            tags=[Tag(name="Java", category="技能")]
        )
    ]
    
    job = JobRequirement(
        position_name="Python工程师",
        requirements="精通Python"
    )
    
    # 初始化服务
    matching_service = MatchingService()
    
    # 排序简历
    ranked_resumes = matching_service.rank_resumes(resumes, job)
    
    # 验证结果
    assert len(ranked_resumes) == 2
    assert ranked_resumes[0]["score"] >= ranked_resumes[1]["score"]
    assert "details" in ranked_resumes[0]
    assert "recommendations" in ranked_resumes[0]
