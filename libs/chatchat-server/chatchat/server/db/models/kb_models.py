from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from ..base import Base

class KnowledgeBase(Base):
    __tablename__ = 'knowledge_base'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    kb_name = Column(String(255), nullable=False, unique=True, comment="知识库名称")
    kb_intro = Column(Text, comment="知识库介绍")
    vs_type = Column(String(255), comment="向量库类型")
    embed_model = Column(String(255), comment="嵌入模型名称")
    file_count = Column(Integer, default=0, comment="文件数量")
    create_time = Column(DateTime, default=datetime.now, comment="创建时间")
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment="更新时间")
    
    files = relationship("KnowledgeFile", back_populates="kb", cascade="all, delete-orphan")

class KnowledgeFile(Base):
    __tablename__ = 'knowledge_file'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    kb_id = Column(Integer, ForeignKey('knowledge_base.id'), nullable=False)
    filename = Column(String(255), nullable=False, comment="文件名")
    file_path = Column(String(255), nullable=False, comment="文件路径")
    file_type = Column(String(50), comment="文件类型")
    file_status = Column(Integer, default=0, comment="文件状态，0：待处理，1：处理中，2：已处理，-1：处理失败")
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    kb = relationship("KnowledgeBase", back_populates="files")