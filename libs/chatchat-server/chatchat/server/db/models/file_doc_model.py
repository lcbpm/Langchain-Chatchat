from sqlalchemy import Column, Integer, String, JSON, DateTime
from datetime import datetime
from ..base import Base

class FileDocModel(Base):
    __tablename__ = 'file_doc'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    kb_name = Column(String(255), nullable=False)
    file_name = Column(String(255), nullable=False)
    doc_id = Column(String(255), nullable=False)
    meta_data = Column(JSON, nullable=True)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)