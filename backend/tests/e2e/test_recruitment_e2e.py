import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_complete_recruitment_flow_e2e(driver):
    # 1. 登录系统
    driver.get("http://localhost:5173/login")
    driver.find_element(By.NAME, "username").send_keys("hr@example.com")
    driver.find_element(By.NAME, "password").send_keys("password123")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # 等待跳转到首页
    WebDriverWait(driver, 10).until(
        EC.url_to_be("http://localhost:5173/dashboard")
    )
    
    # 2. 创建招聘需求
    driver.find_element(By.LINK_TEXT, "创建招聘需求").click()
    driver.find_element(By.NAME, "position_name").send_keys("Python高级工程师")
    driver.find_element(By.NAME, "department").send_keys("技术部")
    driver.find_element(By.NAME, "responsibilities").send_keys(
        "负责后端微服务架构设计和开发"
    )
    driver.find_element(By.NAME, "requirements").send_keys(
        "1. 精通Python开发，5年以上经验\n2. 熟悉微服务架构\n3. 具有大型项目经验"
    )
    driver.find_element(By.NAME, "salary_range").send_keys("35k-50k")
    driver.find_element(By.NAME, "location").send_keys("上海")
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
    
    # 等待创建成功提示
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "el-message--success"))
    )
    
    # 3. 上传简历
    driver.find_element(By.LINK_TEXT, "简历管理").click()
    file_input = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
    file_input.send_keys("/path/to/test/resume.pdf")
    
    # 等待上传完成和解析结果
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.CLASS_NAME, "talent-portrait"))
    )
    
    # 4. 查看匹配结果
    driver.find_element(By.LINK_TEXT, "查看匹配").click()
    
    # 等待匹配结果加载
    match_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "match-item"))
    )
    assert len(match_items) > 0
    
    # 5. 安排面试
    driver.find_element(By.CSS_SELECTOR, ".match-item:first-child .schedule-btn").click()
    
    # 选择面试时间
    driver.find_element(By.NAME, "interview_time").send_keys("2025-03-01 14:00")
    driver.find_element(By.CSS_SELECTOR, ".interviewer-select").click()
    driver.find_element(By.CSS_SELECTOR, ".el-select-dropdown__item").click()
    
    driver.find_element(By.CSS_SELECTOR, ".confirm-schedule-btn").click()
    
    # 等待面试安排成功提示
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "el-message--success"))
    )
    
    # 6. 验证面试列表
    driver.find_element(By.LINK_TEXT, "面试管理").click()
    interview_items = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CLASS_NAME, "interview-item"))
    )
    assert len(interview_items) > 0
    
    # 验证面试状态
    status_element = driver.find_element(By.CLASS_NAME, "interview-status")
    assert "待面试" in status_element.text
