from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class KnowledgeBaseSchema(BaseModel):
    kb_name: str = Field(..., description="知识库名称")
    kb_intro: Optional[str] = Field(None, description="知识库介绍")
    vs_type: Optional[str] = Field(None, description="向量库类型")
    embed_model: Optional[str] = Field(None, description="嵌入模型名称")
    file_count: int = Field(default=0, description="文件数量")
    create_time: datetime = Field(default_factory=datetime.now, description="创建时间")
    update_time: datetime = Field(default_factory=datetime.now, description="更新时间")

    class Config:
        from_attributes = True