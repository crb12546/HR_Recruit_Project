"""
Gunicorn配置文件
用于生产环境部署
"""
import os
import multiprocessing

# 绑定的IP和端口
bind = os.getenv("APP_HOST", "0.0.0.0") + ":" + os.getenv("APP_PORT", "8000")

# 工作进程数
workers = int(os.getenv("GUNICORN_WORKERS", multiprocessing.cpu_count() * 2 + 1))

# 工作模式
worker_class = "uvicorn.workers.UvicornWorker"

# 超时时间
timeout = int(os.getenv("GUNICORN_TIMEOUT", "120"))

# 最大请求数
max_requests = int(os.getenv("GUNICORN_MAX_REQUESTS", "1000"))
max_requests_jitter = int(os.getenv("GUNICORN_MAX_REQUESTS_JITTER", "50"))

# 日志配置
accesslog = os.getenv("GUNICORN_ACCESS_LOG", "logs/access.log")
errorlog = os.getenv("GUNICORN_ERROR_LOG", "logs/error.log")
loglevel = os.getenv("GUNICORN_LOG_LEVEL", "info")

# 进程名称
proc_name = "hr_recruitment_backend"

# 守护进程模式
daemon = os.getenv("GUNICORN_DAEMON", "false").lower() == "true"

# 预加载应用
preload_app = True

# 优雅重启
graceful_timeout = int(os.getenv("GUNICORN_GRACEFUL_TIMEOUT", "30"))

# 保持连接
keepalive = int(os.getenv("GUNICORN_KEEPALIVE", "2"))

# 启动前钩子
def on_starting(server):
    """服务启动前执行"""
    print("Gunicorn服务启动中...")

# 启动后钩子
def when_ready(server):
    """服务启动后执行"""
    print(f"Gunicorn服务已启动 (workers: {workers}, bind: {bind})")
