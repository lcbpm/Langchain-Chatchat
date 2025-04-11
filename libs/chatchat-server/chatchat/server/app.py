from fastapi import FastAPI
from chatchat.server.db.session import init_database

def create_app():
    app = FastAPI(
        title="ChatChat API Server",
        version="0.1.0"
    )
    
    # 初始化数据库
    init_database()
    
    # 注册路由
    from chatchat.server.api import api_router
    app.include_router(api_router)
    
    return app

app = create_app()