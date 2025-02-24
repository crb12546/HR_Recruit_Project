"""验证数据库连接"""
from sqlalchemy import create_engine, text
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def verify_database():
    """验证数据库连接"""
    print('验证数据库连接...')
    url = os.getenv('SQLALCHEMY_DATABASE_URL')
    print(f'数据库URL: {url}')

    engine = create_engine(url)
    with engine.connect() as conn:
        result = conn.execute(text('SELECT 1'))
        print('✓ 数据库连接成功')

if __name__ == '__main__':
    verify_database()
