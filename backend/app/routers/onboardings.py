"""入职管理路由"""
import os
import logging
from fastapi import APIRouter, Depends, HTTPException, Body, Request
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List, Dict, Any
from datetime import datetime
from app.database import get_db
from app.models.onboarding import Onboarding, OnboardingTask
from app.models.resume import Resume
from app.models.job_requirement import JobRequirement
from app.services.gpt import GPTService
from app.utils.db_utils import safe_commit

# 获取日志记录器
logger = logging.getLogger("hr_recruitment")

router = APIRouter(prefix="/api/v1/onboardings", tags=["onboardings"])

@router.post("", status_code=201)
async def create_onboarding(
    request: Request,
    onboarding_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """创建入职记录"""
    try:
        # 记录请求数据
        logger.info(f"创建入职记录请求: {onboarding_data}")
        
        # 验证必填字段
        required_fields = ["resume_id", "job_requirement_id", "offer_date"]
        for field in required_fields:
            if field not in onboarding_data:
                raise HTTPException(status_code=400, detail=f"缺少必填字段: {field}")
        
        # 验证简历存在
        resume_id = onboarding_data.get("resume_id")
        resume = db.query(Resume).filter(Resume.id == resume_id).first()
        if not resume:
            raise HTTPException(status_code=404, detail=f"简历不存在 (ID: {resume_id})")
            
        # 验证职位存在
        job_id = onboarding_data.get("job_requirement_id")
        job = db.query(JobRequirement).filter(JobRequirement.id == job_id).first()
        if not job:
            raise HTTPException(status_code=404, detail=f"招聘需求不存在 (ID: {job_id})")
            
        # 解析日期
        try:
            offer_date = datetime.fromisoformat(onboarding_data.get("offer_date"))
            start_date = datetime.fromisoformat(onboarding_data.get("start_date")) if onboarding_data.get("start_date") else None
            probation_end_date = datetime.fromisoformat(onboarding_data.get("probation_end_date")) if onboarding_data.get("probation_end_date") else None
        except (ValueError, TypeError):
            raise HTTPException(status_code=400, detail="日期格式不正确，请使用ISO格式（如：2025-03-01T00:00:00）")
            
        # 创建入职记录
        onboarding = Onboarding(
            resume_id=resume_id,
            job_requirement_id=job_id,
            status=onboarding_data.get("status", "pending"),
            offer_date=offer_date,
            start_date=start_date,
            probation_end_date=probation_end_date,
            department=onboarding_data.get("department", job.department if job else None),
            position=onboarding_data.get("position", job.position_name if job else None),
            salary=onboarding_data.get("salary"),
            notes=onboarding_data.get("notes")
        )
        
        # 保存到数据库
        db.add(onboarding)
        if not safe_commit(db, "创建入职记录失败"):
            raise HTTPException(status_code=500, detail="数据库保存失败")
        
        db.refresh(onboarding)
        
        # 生成入职任务
        if onboarding_data.get("generate_tasks", True):
            generate_onboarding_tasks(db, onboarding)
        
        # 记录成功创建
        logger.info(f"成功创建入职记录: ID={onboarding.id}, 简历ID={resume_id}, 职位ID={job_id}")
        
        return onboarding.to_dict()
        
    except HTTPException:
        raise
    except SQLAlchemyError as e:
        logger.error(f"数据库错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"数据库操作失败: {str(e)}"
        )
    except Exception as e:
        logger.error(f"创建入职记录失败: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"创建入职记录失败: {str(e)}"
        )

@router.get("")
async def list_onboardings(
    db: Session = Depends(get_db)
):
    """获取入职记录列表"""
    try:
        onboardings = db.query(Onboarding).all()
        return {"onboardings": [onboarding.to_dict() for onboarding in onboardings]}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取入职记录列表失败: {str(e)}"
        )

@router.get("/{onboarding_id}")
async def get_onboarding(
    onboarding_id: int,
    db: Session = Depends(get_db)
):
    """获取入职记录详情"""
    try:
        onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
        if not onboarding:
            raise HTTPException(status_code=404, detail="入职记录不存在")
            
        # 获取入职任务
        tasks = db.query(OnboardingTask).filter(OnboardingTask.onboarding_id == onboarding_id).all()
        
        result = onboarding.to_dict()
        result["tasks"] = [task.to_dict() for task in tasks]
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"获取入职记录详情失败: {str(e)}"
        )

@router.put("/{onboarding_id}")
async def update_onboarding(
    onboarding_id: int,
    onboarding_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """更新入职记录"""
    try:
        onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
        if not onboarding:
            raise HTTPException(status_code=404, detail="入职记录不存在")
            
        # 更新字段
        if "status" in onboarding_data:
            onboarding.status = onboarding_data["status"]
            
        if "start_date" in onboarding_data:
            try:
                onboarding.start_date = datetime.fromisoformat(onboarding_data["start_date"]) if onboarding_data["start_date"] else None
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="入职日期格式不正确")
                
        if "probation_end_date" in onboarding_data:
            try:
                onboarding.probation_end_date = datetime.fromisoformat(onboarding_data["probation_end_date"]) if onboarding_data["probation_end_date"] else None
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="试用期结束日期格式不正确")
                
        if "department" in onboarding_data:
            onboarding.department = onboarding_data["department"]
            
        if "position" in onboarding_data:
            onboarding.position = onboarding_data["position"]
            
        if "salary" in onboarding_data:
            onboarding.salary = onboarding_data["salary"]
            
        if "notes" in onboarding_data:
            onboarding.notes = onboarding_data["notes"]
            
        # 保存到数据库
        db.commit()
        db.refresh(onboarding)
        
        return onboarding.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新入职记录失败: {str(e)}"
        )

@router.post("/{onboarding_id}/tasks")
async def create_onboarding_task(
    onboarding_id: int,
    task_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """创建入职任务"""
    try:
        # 验证入职记录存在
        onboarding = db.query(Onboarding).filter(Onboarding.id == onboarding_id).first()
        if not onboarding:
            raise HTTPException(status_code=404, detail="入职记录不存在")
            
        # 解析截止日期
        deadline = None
        if task_data.get("deadline"):
            try:
                deadline = datetime.fromisoformat(task_data.get("deadline"))
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="截止日期格式不正确")
                
        # 创建任务
        task = OnboardingTask(
            onboarding_id=onboarding_id,
            name=task_data.get("name"),
            description=task_data.get("description"),
            status=task_data.get("status", "pending"),
            deadline=deadline
        )
        
        # 保存到数据库
        db.add(task)
        db.commit()
        db.refresh(task)
        
        return task.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"创建入职任务失败: {str(e)}"
        )

@router.put("/tasks/{task_id}")
async def update_onboarding_task(
    task_id: int,
    task_data: Dict[str, Any] = Body(...),
    db: Session = Depends(get_db)
):
    """更新入职任务"""
    try:
        task = db.query(OnboardingTask).filter(OnboardingTask.id == task_id).first()
        if not task:
            raise HTTPException(status_code=404, detail="入职任务不存在")
            
        # 更新字段
        if "name" in task_data:
            task.name = task_data["name"]
            
        if "description" in task_data:
            task.description = task_data["description"]
            
        if "status" in task_data:
            task.status = task_data["status"]
            # 如果任务完成，记录完成时间
            if task_data["status"] == "completed" and not task.completed_at:
                task.completed_at = datetime.utcnow()
            # 如果任务从完成状态变为其他状态，清除完成时间
            elif task_data["status"] != "completed" and task.completed_at:
                task.completed_at = None
                
        if "deadline" in task_data:
            try:
                task.deadline = datetime.fromisoformat(task_data["deadline"]) if task_data["deadline"] else None
            except (ValueError, TypeError):
                raise HTTPException(status_code=400, detail="截止日期格式不正确")
                
        # 保存到数据库
        db.commit()
        db.refresh(task)
        
        return task.to_dict()
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"更新入职任务失败: {str(e)}"
        )

def generate_onboarding_tasks(db: Session, onboarding: Onboarding):
    """生成入职任务"""
    try:
        # 获取职位信息
        job = db.query(JobRequirement).filter(JobRequirement.id == onboarding.job_requirement_id).first()
        
        # 初始化GPT服务
        gpt_service = GPTService()
        
        # 测试环境使用默认任务
        if os.getenv("ENV") == "test":
            default_tasks = [
                {"name": "签署劳动合同", "description": "与HR签署正式劳动合同", "deadline": onboarding.start_date},
                {"name": "办理入职手续", "description": "提交个人证件复印件，填写入职表格", "deadline": onboarding.start_date},
                {"name": "领取办公设备", "description": "领取笔记本电脑、门禁卡等办公设备", "deadline": onboarding.start_date},
                {"name": "参加入职培训", "description": "参加公司文化、规章制度等入职培训", "deadline": onboarding.start_date},
                {"name": "部门介绍", "description": "了解部门结构、同事和工作职责", "deadline": onboarding.start_date}
            ]
            
            for task_data in default_tasks:
                task = OnboardingTask(
                    onboarding_id=onboarding.id,
                    name=task_data["name"],
                    description=task_data["description"],
                    status="pending",
                    deadline=task_data.get("deadline")
                )
                db.add(task)
                
            db.commit()
            return
            
        # 构建提示词
        prompt = f"""
        请根据以下职位信息，生成一个入职流程任务清单。
        要求：
        1. 任务应该包括入职前准备、入职当天和入职后跟进等阶段
        2. 每个任务包含名称和描述两个字段
        3. 以JSON数组格式返回，如[{{"name": "任务名称", "description": "任务描述"}}]
        4. 使用中文
        5. 返回5-8个任务
        
        职位信息：
        {job.position_name if job else "未知职位"}
        {job.department if job else ""}
        {job.responsibilities if job else ""}
        """
        
        # 调用GPT-4 API
        response = gpt_service.openai.chat.completions.create(
            model=gpt_service.model,
            messages=[
                {"role": "system", "content": "你是一位专业的HR入职管理专家，擅长设计入职流程和任务清单。"},
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
        tasks = result.get("tasks", [])
        
        # 创建任务
        for task_data in tasks:
            task = OnboardingTask(
                onboarding_id=onboarding.id,
                name=task_data["name"],
                description=task_data["description"],
                status="pending"
            )
            db.add(task)
            
        db.commit()
            
    except Exception as e:
        # 出错时使用默认任务
        default_tasks = [
            {"name": "签署劳动合同", "description": "与HR签署正式劳动合同"},
            {"name": "办理入职手续", "description": "提交个人证件复印件，填写入职表格"},
            {"name": "领取办公设备", "description": "领取笔记本电脑、门禁卡等办公设备"},
            {"name": "参加入职培训", "description": "参加公司文化、规章制度等入职培训"},
            {"name": "部门介绍", "description": "了解部门结构、同事和工作职责"}
        ]
        
        for task_data in default_tasks:
            task = OnboardingTask(
                onboarding_id=onboarding.id,
                name=task_data["name"],
                description=task_data["description"],
                status="pending"
            )
            db.add(task)
            
        db.commit()
