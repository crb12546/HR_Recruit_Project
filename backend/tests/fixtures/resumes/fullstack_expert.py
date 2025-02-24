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

# 全栈技术专家简历内容
content = """个人简历

基本信息
姓名：李明远
性别：男
年龄：35岁
电话：136xxxx8888
邮箱：lmy@example.com
现居地：北京市朝阳区

教育背景
2008-2012  清华大学
软件工程 | 本科
2012-2015  北京大学
计算机科学与技术 | 硕士

工作经验
2019-至今  小红书
技术总监/CTO
• 主导公司技术架构升级，引入微服务和云原生架构
• 带领50人研发团队，完成电商和社区核心功能开发
• 优化系统性能，支持日活用户从100万增长到1000万
• 建立DevOps团队，实现全自动化部署和监控

2015-2019  美团
高级全栈工程师
• 负责外卖平台核心模块开发，包括订单系统和支付系统
• 设计实现商家端SaaS系统，服务超过100万商家
• 主导前端技术栈从jQuery迁移到Vue.js
• 开发分布式任务调度系统，处理每日千万级订单

专业技能
• 前端：Vue.js (5年)，React，TypeScript，Webpack
• 后端：Python，Java，Node.js，Go
• 框架：FastAPI，Spring Boot，Express，Django
• 数据库：MySQL，MongoDB，Redis，Elasticsearch
• 云服务：阿里云，腾讯云，Docker，K8s
• DevOps：Jenkins，GitLab CI，Prometheus

项目经验
小红书社区电商平台重构（2020-2021）
• 主导整个技术架构设计和团队管理
• 实现前后端分离，采用Vue.js + FastAPI架构
• 引入微服务架构，提升系统可扩展性
• 优化搜索引擎，提升商品搜索效率200%

美团商家SaaS平台（2017-2019）
• 设计开发商家运营管理系统
• 实现多租户架构，支持商家个性化定制
• 开发实时数据分析系统，助力商家经营决策
• 系统服务超过100万商家，日均订单处理量500万

证书
• 阿里云高级架构师认证
• 腾讯云解决方案架构师认证
• PMP项目管理认证
• CISSP信息安全认证

自我评价
• 10年互联网行业经验，精通全栈开发
• 丰富的技术团队管理和架构设计经验
• 对云原生和微服务架构有深入理解
• 具有创业公司CTO经历，善于技术决策"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'fullstack_expert.pdf'), content)
