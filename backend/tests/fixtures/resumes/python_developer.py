from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.units import inch
import os

def create_resume(filename, content):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4
    
    # 设置中文字体
    c.setFont("Helvetica", 12)
    
    # 写入内容
    y = height - inch
    for line in content.split('\n'):
        if not line.strip():
            y -= 12
            continue
        if line.startswith('个人简历'):
            c.setFont("Helvetica-Bold", 18)
            c.drawString(width/2 - 50, y, line)
            c.setFont("Helvetica", 12)
        elif any(line.startswith(section) for section in ['基本信息', '教育背景', '工作经验', '专业技能', '项目经验', '证书', '自我评价']):
            c.setFont("Helvetica-Bold", 14)
            c.drawString(inch, y, line)
            c.setFont("Helvetica", 12)
        else:
            c.drawString(inch, y, line)
        y -= 14
        if y < inch:
            c.showPage()
            y = height - inch
    
    c.save()

# Python开发工程师简历内容
content = """个人简历

基本信息
姓名：王建国
性别：男
年龄：28岁
电话：135xxxx3456
邮箱：wangjg@example.com
现居地：深圳市南山区

教育背景
2014-2018  华南理工大学
计算机科学与技术 | 本科

工作经验
2021-至今  腾讯云
Python开发工程师
• 负责云函数平台API开发，使用FastAPI框架
• 开发自动化部署系统，提升部署效率200%
• 设计实现分布式日志收集系统
• 优化API性能，平均响应时间降低40%

2019-2021  深信服科技
后端开发工程师
• 参与安全管理平台后端开发
• 使用Python开发自动化测试框架
• 实现系统监控告警功能

专业技能
• 编程语言：Python (4年经验)，Go (基础)
• Web框架：FastAPI (3年)，Django，Flask
• 数据库：PostgreSQL，MongoDB，Redis
• 消息队列：RabbitMQ，Kafka
• 容器技术：Docker，Kubernetes
• 开发工具：Git，Jenkins，Prometheus

项目经验
腾讯云函数计算平台（2022-2023）
• 使用FastAPI重构API网关
• 实现函数触发器系统
• 开发函数监控系统
• 日均处理请求量超过500万

深信服安全管理平台（2019-2021）
• 开发安全策略配置模块
• 实现设备管理系统
• 设计日志分析系统
• 服务超过1000家企业客户

证书
• 腾讯云开发者认证
• AWS认证开发工程师
• Python高级开发工程师认证

自我评价
• 4年Python开发经验，精通FastAPI框架
• 具有大型项目开发和优化经验
• 良好的问题分析和解决能力
• 持续学习新技术，保持技术更新"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'python_developer.pdf'), content)
