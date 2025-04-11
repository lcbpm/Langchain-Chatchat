from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from sqlalchemy import create_engine, MetaData
from chatchat.settings import BasicSettings

# 创建带命名约束的 MetaData
naming_convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

# 创建基类
class Base(DeclarativeBase):
    metadata = MetaData(naming_convention=naming_convention)

# 创建数据库引擎
engine = create_engine(BasicSettings().SQLALCHEMY_DATABASE_URI)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
