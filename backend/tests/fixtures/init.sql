-- 初始化测试数据库
CREATE DATABASE IF NOT EXISTS hr_recruit_test;
USE hr_recruit_test;

-- 创建标签表
CREATE TABLE IF NOT EXISTS tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    category VARCHAR(20) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 创建初始标签数据
INSERT INTO tags (name, category) VALUES
('Python', '技能'),
('FastAPI', '技能'),
('Vue.js', '技能'),
('MySQL', '技能'),
('3-5年', '经验'),
('5-8年', '经验'),
('本科', '学历'),
('硕士', '学历');
