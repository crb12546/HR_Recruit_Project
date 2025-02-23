import pytest
from unittest.mock import Mock, patch
from app.services.matching import MatchingService
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement

@pytest.fixture
def mock_db():
    db = Mock()
    return db

@pytest.fixture
def mock_gpt():
    with patch('app.services.gpt.GPTService') as mock:
        yield mock

def test_find_matching_resumes(mock_db, mock_gpt):
    """测试查找匹配简历"""
    # 准备测试数据
    job = JobRequirement(
        id=1,
        position_name="Python工程师",
        department="技术部",
        responsibilities="开发后端服务",
        skills=["Python", "FastAPI", "MySQL"],
        education="本科及以上",
        experience="3-5年",
        salary_min=20000,
        salary_max=30000,
        location=["北京", "海淀区"],
        status="active"
    )
    
    resumes = [
        Resume(id=1, candidate_name="张三"),
        Resume(id=2, candidate_name="李四"),
        Resume(id=3, candidate_name="王五")
    ]
    
    # Mock数据库查询
    mock_db.query.return_value.filter.return_value.first.return_value = job
    mock_db.query.return_value.all.return_value = resumes
    
    # Mock GPT服务
    mock_scores = [
        {
            "total_score": 90,
            "skill_score": {"score": 95, "reason": "技能匹配度高"},
            "experience_score": {"score": 85, "reason": "经验充足"},
            "education_score": {"score": 100, "reason": "学历符合"},
            "responsibility_score": {"score": 88, "reason": "有相关经验"}
        },
        {
            "total_score": 75,
            "skill_score": {"score": 80, "reason": "部分技能匹配"},
            "experience_score": {"score": 70, "reason": "经验略少"},
            "education_score": {"score": 100, "reason": "学历符合"},
            "responsibility_score": {"score": 75, "reason": "经验相关"}
        },
        {
            "total_score": 60,
            "skill_score": {"score": 65, "reason": "技能欠缺"},
            "experience_score": {"score": 55, "reason": "经验不足"},
            "education_score": {"score": 80, "reason": "学历达标"},
            "responsibility_score": {"score": 60, "reason": "经验有限"}
        }
    ]
    
    mock_gpt.return_value.calculate_match_score.side_effect = mock_scores
    
    # 执行测试
    service = MatchingService(mock_db)
    matches = service.find_matching_resumes(1, limit=2)
    
    # 验证结果
    assert len(matches) == 2
    assert matches[0]["match_score"]["total_score"] == 90
    assert matches[1]["match_score"]["total_score"] == 75

def test_find_matching_jobs(mock_db, mock_gpt):
    """测试查找匹配职位"""
    # 准备测试数据
    resume = Resume(
        id=1,
        candidate_name="张三",
        file_url="test.pdf",
        file_type="application/pdf",
        ocr_content="熟练掌握Python...",
        parsed_content="技能：Python, FastAPI...",
        talent_portrait="优秀的后端工程师"
    )
    
    jobs = [
        JobRequirement(
            id=1,
            position_name="高级Python工程师",
            status="active"
        ),
        JobRequirement(
            id=2,
            position_name="全栈工程师",
            status="active"
        ),
        JobRequirement(
            id=3,
            position_name="后端工程师",
            status="active"
        )
    ]
    
    # Mock数据库查询
    mock_db.query.return_value.filter.return_value.first.return_value = resume
    mock_db.query.return_value.filter.return_value.all.return_value = jobs
    
    # Mock GPT服务
    mock_scores = [
        {
            "total_score": 95,
            "skill_score": {"score": 98, "reason": "技能完全匹配"},
            "experience_score": {"score": 90, "reason": "经验丰富"},
            "education_score": {"score": 100, "reason": "学历优秀"},
            "responsibility_score": {"score": 92, "reason": "经验对口"}
        },
        {
            "total_score": 80,
            "skill_score": {"score": 85, "reason": "全栈技能部分匹配"},
            "experience_score": {"score": 75, "reason": "全栈经验有限"},
            "education_score": {"score": 100, "reason": "学历优秀"},
            "responsibility_score": {"score": 78, "reason": "需要补充前端经验"}
        },
        {
            "total_score": 88,
            "skill_score": {"score": 90, "reason": "后端技能匹配"},
            "experience_score": {"score": 85, "reason": "经验充足"},
            "education_score": {"score": 100, "reason": "学历优秀"},
            "responsibility_score": {"score": 85, "reason": "经验相关"}
        }
    ]
    
    mock_gpt.return_value.calculate_match_score.side_effect = mock_scores
    
    # 执行测试
    service = MatchingService(mock_db)
    matches = service.find_matching_jobs(1, limit=2)
    
    # 验证结果
    assert len(matches) == 2
    assert matches[0]["match_score"]["total_score"] == 95
    assert matches[1]["match_score"]["total_score"] == 88

def test_matching_with_invalid_resume(mock_db):
    """测试无效简历ID的情况"""
    # Mock数据库查询返回None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    service = MatchingService(mock_db)
    with pytest.raises(ValueError, match="简历不存在"):
        service.find_matching_jobs(999)

def test_matching_with_invalid_job(mock_db):
    """测试无效职位ID的情况"""
    # Mock数据库查询返回None
    mock_db.query.return_value.filter.return_value.first.return_value = None
    
    service = MatchingService(mock_db)
    with pytest.raises(ValueError, match="职位不存在"):
        service.find_matching_resumes(999)
