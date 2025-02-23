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
        elif any(line.startswith(section) for section in ['基本信息', '教育背景', '工作经验', '专业技能', '研究成果', '项目经验', '证书', '自我评价']):
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

# AI算法工程师简历内容
content = """个人简历

基本信息
姓名：林智远
性别：男
年龄：28岁
电话：135xxxx2345
邮箱：linzy@example.com
现居地：北京市海淀区

教育背景
2018-2021  中国科学院大学
人工智能 | 硕士
• 研究方向：深度学习，计算机视觉
• GPA：3.9/4.0

2014-2018  北京航空航天大学
计算机科学与技术 | 本科
• GPA：3.8/4.0

工作经验
2021-至今  商汤科技
AI算法工程师
• 负责计算机视觉算法研发
• 开发目标检测和图像分割模型
• 优化深度学习模型性能
• 指导初级算法工程师

2020-2021  百度
算法实习生
• 参与自然语言处理项目
• 实现BERT模型fine-tuning
• 开发文本分类算法

专业技能
• 编程语言：Python，C++
• 深度学习：PyTorch，TensorFlow
• 机器学习：scikit-learn，XGBoost
• 计算机视觉：OpenCV，MMDetection
• 自然语言处理：Transformers，NLTK
• 开发工具：Git，Docker，Linux

研究成果
• 发表CVPR论文1篇，ICCV论文1篇
• 申请计算机视觉相关专利2项
• 开源深度学习项目获1000+星标

项目经验
多模态商品识别系统（2022-2023）
• 设计实现商品检测算法
• 开发多模态特征融合模型
• 优化模型推理性能
• 准确率提升15%

行人重识别系统（2021-2022）
• 开发行人检测和跟踪算法
• 实现特征提取网络
• 优化模型训练流程
• 部署模型到边缘设备

证书
• 深度学习专业证书（Coursera）
• NVIDIA深度学习认证
• 华为AI开发者认证

自我评价
• 3年深度学习算法开发经验
• 熟悉计算机视觉和NLP领域
• 具有算法优化和部署经验
• 良好的研究和工程能力"""

if __name__ == '__main__':
    output_dir = os.path.dirname(__file__)
    create_resume(os.path.join(output_dir, 'ai_engineer.pdf'), content)
