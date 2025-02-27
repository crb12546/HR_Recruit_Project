"""面试管理路由"""
import os
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from datetime import datetime
from app.database import get_db
from app.models.interview import Interview
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.models.user import User
from app.services.gpt import GPTService

router = APIRouter(prefix="/api/v1/interviews", tags=["interviews"])

@router.post("", status_code=201)
async def schedule_interview(
    interview_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """安排面试"""
    try:
        # 验证简历存在
        resume = db.query(Resume).filter(Resume.id == interview_data.get("resume_id")).first()
        if not resume:
            raise HTTPException(status_code=404, detail="简历不存在")
            
        # 验证职位存在
        job = db.query(JobRequirement).filter(JobRequirement.id == interview_data.get("job_requirement_id")).first()
        if not job:
            raise HTTPException(status_code=404, detail="招聘需求不存在")
            
        # 验证面试官存在
        interviewer = db.query(User).filter(User.id == interview_data.get("interviewer_id")).first()
        if not interviewer:
            raise HTTPException(status_code=404, detail="面试官不存在")
            
        # 解析面试时间
        try:
            interview_time = datetime.fromisoformat(interview_data.get("interview_time"))
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="面试时间格式不正确，请使用ISO格式（如：2025-03-01T14:00:00）")
            
        # 创建面试记录
        interview = Interview(
            resume_id=interview_data.get("resume_id"),
            job_requirement_id=interview_data.get("job_requirement_id"),
            interviewer_id=interview_data.get("interviewer_id"),
            interview_time=interview_time,
            status="scheduled"
        )
        
        # 保存到数据库
        db.add(interview)
        db.commit()
        db.refresh(interview)
        
        return interview_to_dict(interview)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"安排面试失败: {str(e)}"
        )

@router.get("")
async def list_interviews(
    db: Session = Depends(get_db)
):
    """获取面试列表"""
    try:
        interviews = db.query(Interview).all()
        return {"interviews": [interview_to_dict(interview) for interview in interviews]}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取面试列表失败: {str(e)}"
        )

@router.get("/{interview_id}")
async def get_interview(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """获取面试详情"""
    try:
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="面试不存在")
            
        return interview_to_dict(interview)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取面试详情失败: {str(e)}"
        )

@router.post("/{interview_id}/questions")
async def generate_interview_questions(
    interview_id: int,
    db: Session = Depends(get_db)
):
    """生成面试问题"""
    try:
        # 获取面试记录
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="面试不存在")
            
        # 获取简历和职位信息
        resume = db.query(Resume).filter(Resume.id == interview.resume_id).first()
        job = db.query(JobRequirement).filter(JobRequirement.id == interview.job_requirement_id).first()
        
        if not resume or not job:
            raise HTTPException(status_code=404, detail="简历或职位信息不存在")
            
        # 初始化GPT服务
        gpt_service = GPTService()
        
        # 生成面试问题
        questions = generate_questions(gpt_service, resume, job)
        
        return {"questions": questions}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"生成面试问题失败: {str(e)}"
        )

@router.post("/{interview_id}/feedback")
async def submit_interview_feedback(
    interview_id: int,
    feedback_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """提交面试反馈"""
    try:
        # 获取面试记录
        interview = db.query(Interview).filter(Interview.id == interview_id).first()
        if not interview:
            raise HTTPException(status_code=404, detail="面试不存在")
            
        # 更新面试反馈
        interview.feedback = feedback_data.get("feedback")
        interview.score = feedback_data.get("score")
        interview.status = feedback_data.get("status", "completed")
        
        # 保存到数据库
        db.commit()
        db.refresh(interview)
        
        return interview_to_dict(interview)
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"提交面试反馈失败: {str(e)}"
        )

def interview_to_dict(interview: Interview) -> Dict[str, Any]:
    """将Interview对象转换为字典"""
    return {
        "id": interview.id,
        "resume_id": interview.resume_id,
        "job_requirement_id": interview.job_requirement_id,
        "interviewer_id": interview.interviewer_id,
        "interview_time": interview.interview_time.isoformat() if interview.interview_time else None,
        "status": interview.status,
        "feedback": interview.feedback,
        "score": interview.score,
        "created_at": interview.created_at.isoformat() if interview.created_at else None,
        "updated_at": interview.updated_at.isoformat() if interview.updated_at else None
    }

def generate_questions(gpt_service: GPTService, resume: Resume, job: JobRequirement) -> List[Dict[str, str]]:
    """生成面试问题"""
    try:
        # 测试环境使用模拟数据
        if os.getenv("ENV") == "test":
            return [
                {"content": "请介绍一下您在Python方面的经验和项目？", "type": "技术能力"},
                {"content": "您如何理解微服务架构？请分享您的实践经验。", "type": "架构设计"},
                {"content": "您参与过的最大规模项目是什么？您在其中担任什么角色？", "type": "项目经验"},
                {"content": "您如何处理高并发场景下的性能优化？", "type": "技术深度"},
                {"content": "您对未来的职业规划是什么？", "type": "个人发展"}
            ]
            
        # 构建提示词
        prompt = f"""
        请根据以下职位要求和候选人简历，生成5-8个针对性的面试问题。
        要求：
        1. 问题应该覆盖技术能力、项目经验、解决问题能力等方面
        2. 问题应该与职位要求和候选人背景高度相关
        3. 以JSON数组格式返回，每个问题包含content和type两个字段
        4. 使用中文提问
        
        职位要求：
        {job.position_name}
        {job.responsibilities}
        {job.requirements}
        
        候选人简历：
        {resume.ocr_content}
        """
        
        # 调用GPT-4 API
        response = gpt_service.openai.chat.completions.create(
            model=gpt_service.model,
            messages=[
                {"role": "system", "content": "你是一位专业的技术面试官，擅长根据职位要求和候选人背景生成有针对性的面试问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000,
            response_format={"type": "json_object"}
        )
        
        # 解析JSON响应
        import json
        content = response.choices[0].message.content
        result = json.loads(content)
        
        return result.get("questions", [])
            
    except Exception as e:
        # 出错时返回默认问题
        return [
            {"content": "请介绍一下您的工作经验和技能？", "type": "基本情况"},
            {"content": "您为什么对我们公司的这个职位感兴趣？", "type": "求职动机"},
            {"content": "您认为自己最大的优势是什么？", "type": "自我评价"}
        ]
