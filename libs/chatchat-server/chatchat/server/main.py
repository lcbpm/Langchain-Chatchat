from chatchat.server.db.session import init_database

def main():
    # 确保数据库表已创建
    init_database()
    # ... 其他启动代码 ...