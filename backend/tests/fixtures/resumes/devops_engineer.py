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

# DevOps工程师简历内容
content = """个人简历

基本信息
姓名：郑云峰
性别：男
年龄：33岁
电话：133xxxx6789
邮箱：zhengyf@example.com
现居地：深圳市南山区

教育背景
2010-2014  华中科技大学
计算机科学与技术 | 本科

工作经验
2020-至今  腾讯云
高级DevOps工程师
• 负责云原生平台的自动化部署和运维
• 设计实现容器化CI/CD流水线
• 优化部署流程，部署时间缩短70%
• 管理和优化Kubernetes集群

2017-2020  华为云
DevOps工程师
• 开发自动化运维工具和脚本
• 构建微服务监控系统
• 实现自动化测试框架
• 管理多环境部署流程

2014-2017  金山云
运维工程师
• 负责系统运维和监控
• 实现自动化部署脚本
• 参与容器化转型项目

专业技能
• 编程语言：Python，Shell，Go
• 容器技术：Docker，Kubernetes，Helm
• CI/CD工具：Jenkins，GitLab CI，ArgoCD
• 监控工具：Prometheus，Grafana，ELK
• 云平台：腾讯云，华为云，阿里云
• 配置管理：Ansible，Terraform，Puppet
• 版本控制：Git，GitHub，GitLab

项目经验
腾讯云原生平台（2021-2023）
• 设计实现全自动化部署平台
• 开发多集群管理系统
• 实现灰度发布功能
• 支持每日3000+次部署

华为云微服务平台（2018-2020）
• 构建微服务监控体系
• 实现自动化运维平台
• 开发容器管理系统
• 管理超过1000个容器节点

证书
• Kubernetes管理员认证（CKA）
• AWS解决方案架构师认证
• 腾讯云高级架构师认证
• Docker认证工程师

自我评价
• 7年DevOps和自动化部署经验
• 精通云原生技术和自动化工具
• 具有大规模集群管理经验
• 良好的问题排查和解决能力"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'devops_engineer.pdf'), content)
