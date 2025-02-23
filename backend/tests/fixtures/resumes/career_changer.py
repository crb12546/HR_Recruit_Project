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
        elif any(line.startswith(section) for section in ['基本信息', '教育背景', '工作经验', '培训经历', '项目经验', '专业技能', '自我评价']):
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

# 转行程序员简历内容
content = """个人简历

基本信息
姓名：张明华
性别：男
年龄：29岁
电话：138xxxx4567
邮箱：zhangmh@example.com
现居地：成都市武侯区

教育背景
2013-2017  四川大学
市场营销 | 本科

工作经验
2023-至今  成都某科技公司
Python开发工程师
• 参与公司内部管理系统开发
• 使用Python和Django开发后端API
• 编写自动化测试脚本
• 参与代码评审和技术分享

2017-2022  某大型零售企业
营销经理
• 负责产品营销策略制定
• 管理营销团队和预算
• 分析销售数据和市场趋势

培训经历
2022.07-2022.12  Python全栈开发培训
• 系统学习Python编程基础
• Web开发框架Django和Flask
• 数据库设计和SQL编程
• 前端基础知识HTML/CSS/JavaScript

项目经验
企业内部管理系统（2023）
• 使用Python和Django开发后端API
• 实现员工管理、考勤统计功能
• 编写单元测试，提升代码质量
• 优化数据库查询性能

个人项目：销售数据分析工具（2022）
• 使用Python处理Excel数据
• 开发数据可视化界面
• 实现自动生成分析报告
• GitHub开源项目

专业技能
• 编程语言：Python (1年)
• Web框架：Django, Flask
• 数据库：MySQL, SQLite
• 开发工具：Git, VS Code
• 办公软件：精通Excel数据分析
• 英语能力：CET-6

自我评价
• 具有良好的学习能力和解决问题的思维
• 丰富的项目管理和团队协作经验
• 善于数据分析和业务需求理解
• 对编程充满热情，持续学习新技术"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'career_changer.pdf'), content)
