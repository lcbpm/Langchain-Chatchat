from contextlib import contextmanager
from functools import wraps

from sqlalchemy.orm import Session

from chatchat.server.db.base import SessionLocal
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from chatchat.settings import DBSettings

Base = declarative_base()

def init_database():
    """初始化数据库，创建所有表"""
    engine = create_engine(DBSettings().SQLALCHEMY_DATABASE_URI)
    Base.metadata.create_all(engine)

def get_session():
    """获取数据库会话"""
    engine = create_engine(DBSettings().SQLALCHEMY_DATABASE_URI)
    session_factory = sessionmaker(bind=engine)
    return scoped_session(session_factory)

# 确保在应用启动时调用初始化
init_database()


@contextmanager
def session_scope() -> Session:
    """上下文管理器用于自动获取 Session, 避免错误"""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


def with_session(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        with session_scope() as session:
            try:
                result = f(session, *args, **kwargs)
                session.commit()
                return result
            except:
                session.rollback()
                raise

    return wrapper


def get_db() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db0() -> SessionLocal:
    db = SessionLocal()
    return db
