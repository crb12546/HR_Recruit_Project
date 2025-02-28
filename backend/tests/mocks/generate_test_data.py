import json
import os
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_resume_data(count=10):
    """生成测试简历数据"""
    resumes = []
    
    # 候选人姓名列表
    names = ["张三", "李四", "王五", "赵六", "钱七", "孙八", "周九", "吴十", 
             "郑十一", "王十二", "刘十三", "陈十四", "杨十五", "黄十六"]
    
    # 学历列表
    educations = ["本科", "硕士", "博士", "大专", "高中"]
    
    # 技能列表
    all_skills = [
        "Python", "Java", "C++", "JavaScript", "TypeScript", "Go", "Rust",
        "React", "Vue.js", "Angular", "Node.js", "FastAPI", "Django", "Flask",
        "Spring Boot", "MySQL", "PostgreSQL", "MongoDB", "Redis", "Docker",
        "Kubernetes", "AWS", "Azure", "GCP", "Linux", "Git", "CI/CD",
        "微服务", "前端开发", "后端开发", "全栈开发", "DevOps", "数据分析",
        "机器学习", "深度学习", "自然语言处理", "计算机视觉", "大数据"
    ]
    
    # 文件类型列表
    file_types = ["pdf", "docx", "doc"]
    
    for i in range(1, count + 1):
        # 随机选择候选人姓名
        name = random.choice(names)
        names.remove(name)  # 确保姓名不重复
        
        # 随机选择学历
        education = random.choice(educations)
        
        # 随机选择3-6个技能
        skills_count = random.randint(3, 6)
        skills = random.sample(all_skills, skills_count)
        
        # 随机工作经验
        experience = f"{random.randint(1, 10)}年"
        
        # 随机联系电话
        contact = f"138{random.randint(10000000, 99999999)}"
        
        # 随机文件类型
        file_type = random.choice(file_types)
        
        # 构建简历数据
        resume = {
            "id": i,
            "candidate_name": name,
            "file_url": f"https://test-bucket.oss.aliyuncs.com/resume_{i}.{file_type}",
            "file_type": file_type,
            "ocr_content": f"姓名：{name}\n学历：{education}\n技能：{', '.join(skills)}\n工作经验：{experience}\n联系电话：{contact}",
            "parsed_content": {
                "name": name,
                "education": education,
                "skills": skills,
                "experience": experience,
                "contact": contact
            },
            "talent_portrait": f"{name}是一名有{experience}经验的{'全栈' if '全栈' in skills else '开发'}工程师，{education}学历，精通{skills[0]}和{skills[1]}，有良好的{skills[2]}开发能力。"
        }
        
        resumes.append(resume)
    
    return {"resumes": resumes}

def generate_job_data(count=5):
    """生成测试职位数据"""
    jobs = []
    
    # 职位名称列表
    positions = [
        "Python高级工程师", "前端开发工程师", "Java后端工程师", "全栈开发工程师",
        "DevOps工程师", "数据分析师", "机器学习工程师", "产品经理", "UI设计师",
        "测试工程师", "运维工程师", "项目经理", "技术总监"
    ]
    
    # 部门列表
    departments = ["技术部", "产品部", "设计部", "测试部", "运维部", "研发中心"]
    
    # 状态列表
    statuses = ["open", "closed", "draft"]
    
    for i in range(1, count + 1):
        # 随机选择职位名称
        position = random.choice(positions)
        positions.remove(position)  # 确保职位不重复
        
        # 随机选择部门
        department = random.choice(departments)
        
        # 随机薪资范围
        min_salary = random.randint(10, 40)
        max_salary = min_salary + random.randint(5, 20)
        salary_range = f"{min_salary}k-{max_salary}k"
        
        # 随机状态
        status = random.choice(statuses)
        
        # 构建职位数据
        job = {
            "id": i,
            "position_name": position,
            "department": department,
            "job_description": f"负责公司{position.replace('工程师', '').replace('经理', '')}相关系统的开发和维护",
            "requirements": f"1. 精通{position.replace('工程师', '').replace('经理', '')}相关技术\n2. 熟悉相关开发工具和框架\n3. 有{random.randint(1, 8)}年以上开发经验",
            "salary_range": salary_range,
            "status": status
        }
        
        jobs.append(job)
    
    return {"jobs": jobs}

def generate_interview_data(resume_count=10, job_count=5):
    """生成测试面试数据"""
    interviews = []
    
    # 面试状态列表
    statuses = ["scheduled", "completed", "cancelled"]
    
    # 评分列表
    ratings = [None, 1, 2, 3, 4, 5]
    
    # 面试问题模板
    question_templates = [
        "请描述一下你使用{skill}解决过的最复杂的问题？",
        "你如何理解{skill}的核心特性？",
        "你在项目中如何使用{skill}进行开发？",
        "你认为{skill}相比其他类似技术有什么优势？",
        "你如何保证{skill}开发的代码质量？",
        "你如何处理{skill}开发中遇到的性能问题？",
        "你如何与团队协作完成{skill}相关的项目？",
        "你在{skill}方面遇到过哪些挑战，如何解决的？"
    ]
    
    for i in range(1, min(resume_count, job_count) + 5):
        # 随机选择简历ID和职位ID
        resume_id = random.randint(1, resume_count)
        job_id = random.randint(1, job_count)
        
        # 随机面试时间（未来1-30天内）
        days_ahead = random.randint(1, 30)
        interview_time = (datetime.now() + timedelta(days=days_ahead)).replace(
            hour=random.randint(9, 17),
            minute=random.choice([0, 30]),
            second=0,
            microsecond=0
        )
        
        # 随机状态
        status = random.choice(statuses)
        
        # 如果状态是已完成，添加反馈和评分
        feedback = None
        rating = None
        if status == "completed":
            feedback = "候选人表现良好，技术能力符合要求，沟通能力强，团队协作意识好。"
            rating = random.choice(ratings[1:])  # 排除None
        
        # 随机生成3-5个面试问题
        questions_count = random.randint(3, 5)
        skills = ["Python", "Java", "JavaScript", "React", "Vue.js", "FastAPI", "Spring Boot"]
        questions = []
        
        for _ in range(questions_count):
            template = random.choice(question_templates)
            skill = random.choice(skills)
            questions.append(template.format(skill=skill))
        
        # 构建面试数据
        interview = {
            "id": i,
            "resume_id": resume_id,
            "job_requirement_id": job_id,
            "interviewer_id": random.randint(1, 3),
            "interview_time": interview_time.isoformat(),
            "status": status,
            "feedback": feedback,
            "rating": rating,
            "interview_questions": questions
        }
        
        interviews.append(interview)
    
    return {"interviews": interviews}

def generate_onboarding_data(resume_count=10, job_count=5):
    """生成测试入职数据"""
    onboardings = []
    
    # 状态列表
    statuses = ["pending", "in_progress", "completed", "cancelled"]
    
    # 部门列表
    departments = ["技术部", "产品部", "设计部", "测试部", "运维部", "研发中心"]
    
    # 职位列表
    positions = [
        "Python工程师", "前端工程师", "Java工程师", "全栈工程师",
        "DevOps工程师", "数据分析师", "机器学习工程师", "产品经理", "UI设计师",
        "测试工程师", "运维工程师", "项目经理"
    ]
    
    for i in range(1, min(resume_count, job_count) + 3):
        # 随机选择简历ID和职位ID
        resume_id = random.randint(1, resume_count)
        job_id = random.randint(1, job_count)
        
        # 随机部门和职位
        department = random.choice(departments)
        position = random.choice(positions)
        
        # 随机薪资
        salary = f"{random.randint(10, 50)}k"
        
        # 随机日期
        offer_date = (datetime.now() + timedelta(days=random.randint(1, 10))).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        start_date = (offer_date + timedelta(days=random.randint(10, 30))).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        probation_end_date = (start_date + timedelta(days=random.randint(60, 180))).replace(
            hour=0, minute=0, second=0, microsecond=0
        )
        
        # 随机状态
        status = random.choice(statuses)
        
        # 随机备注
        notes = random.choice([
            "需要提前准备开发环境",
            "需要安排入职培训",
            "需要准备工作电脑",
            "需要安排团队欢迎会",
            "需要提前准备工作证件",
            ""
        ])
        
        # 生成入职任务
        tasks = []
        task_templates = [
            {"name": "准备开发电脑", "description": "配置高性能开发笔记本，安装必要的开发软件", "assignee": "IT部门"},
            {"name": "配置开发环境", "description": "安装开发环境和工具", "assignee": "技术部门"},
            {"name": "安排入职培训", "description": "公司制度、文化和业务培训", "assignee": "HR部门"},
            {"name": "办理入职手续", "description": "签署劳动合同，提交个人资料", "assignee": "HR部门"},
            {"name": "安排工位", "description": "准备工位和办公用品", "assignee": "行政部门"},
            {"name": "团队介绍", "description": "向团队介绍新成员，安排团队欢迎会", "assignee": "部门经理"},
            {"name": "项目交接", "description": "安排项目交接和知识分享", "assignee": "技术负责人"}
        ]
        
        # 随机选择3-5个任务
        task_count = random.randint(3, 5)
        selected_tasks = random.sample(task_templates, task_count)
        
        for j, task in enumerate(selected_tasks, 1):
            # 随机截止日期（入职前后5天内）
            days_offset = random.randint(-5, 5)
            deadline = (start_date + timedelta(days=days_offset)).replace(
                hour=0, minute=0, second=0, microsecond=0
            )
            
            # 随机状态
            task_status = random.choice(["pending", "in_progress", "completed"])
            
            # 构建任务数据
            task_data = {
                "id": j,
                "onboarding_id": i,
                "task_name": task["name"],
                "description": task["description"],
                "assignee": task["assignee"],
                "deadline": deadline.isoformat(),
                "status": task_status
            }
            
            tasks.append(task_data)
        
        # 构建入职数据
        onboarding = {
            "id": i,
            "resume_id": resume_id,
            "job_requirement_id": job_id,
            "department": department,
            "position": position,
            "salary": salary,
            "offer_date": offer_date.isoformat(),
            "start_date": start_date.isoformat(),
            "probation_end_date": probation_end_date.isoformat(),
            "status": status,
            "notes": notes,
            "tasks": tasks
        }
        
        onboardings.append(onboarding)
    
    return {"onboardings": onboardings}

def generate_all_test_data():
    """生成所有测试数据"""
    # 创建数据目录
    current_dir = Path(__file__).parent
    data_dir = current_dir / "data"
    os.makedirs(data_dir, exist_ok=True)
    
    # 生成简历数据
    resume_count = 10
    resume_data = generate_resume_data(resume_count)
    with open(data_dir / "mock_resume.json", "w", encoding="utf-8") as f:
        json.dump(resume_data, f, ensure_ascii=False, indent=2)
    
    # 生成职位数据
    job_count = 5
    job_data = generate_job_data(job_count)
    with open(data_dir / "mock_jobs.json", "w", encoding="utf-8") as f:
        json.dump(job_data, f, ensure_ascii=False, indent=2)
    
    # 生成面试数据
    interview_data = generate_interview_data(resume_count, job_count)
    with open(data_dir / "mock_interviews.json", "w", encoding="utf-8") as f:
        json.dump(interview_data, f, ensure_ascii=False, indent=2)
    
    # 生成入职数据
    onboarding_data = generate_onboarding_data(resume_count, job_count)
    with open(data_dir / "mock_onboardings.json", "w", encoding="utf-8") as f:
        json.dump(onboarding_data, f, ensure_ascii=False, indent=2)
    
    print(f"已生成测试数据：")
    print(f"- 简历数据: {resume_count}条")
    print(f"- 职位数据: {job_count}条")
    print(f"- 面试数据: {len(interview_data['interviews'])}条")
    print(f"- 入职数据: {len(onboarding_data['onboardings'])}条")

if __name__ == "__main__":
    generate_all_test_data()
