import importlib
import json
import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlencode
from typing import Dict, Generator, List, Tuple, Union
from chatchat.settings import KBSettings

import chardet
import langchain_community.document_loaders
from langchain.docstore.document import Document
from langchain.text_splitter import MarkdownHeaderTextSplitter, TextSplitter
from langchain_community.document_loaders import JSONLoader, TextLoader
from langchain_community.docstore.in_memory import InMemoryDocstore  # 更新导入
from langchain_community.vectorstores import FAISS  # 更新导入

from datetime import datetime
from pathlib import Path
import os

import re

class KnowledgeFileObj:
    def __init__(self, 
                 filename: str,
                 kb_name: str,
                 ext: str = None,
                 document_loader_name: str = None,
                 text_splitter_name: str = None):
        self.filename = filename
        self.kb_name = kb_name
        self.ext = ext or Path(filename).suffix.lower()
        self.document_loader_name = document_loader_name
        self.text_splitter_name = text_splitter_name
        
    def get_mtime(self) -> datetime:
        """获取文件最后修改时间"""
        return datetime.fromtimestamp(os.path.getmtime(self.filename))
        
    def get_size(self) -> int:
        """获取文件大小（字节）"""
        return os.path.getsize(self.filename)


class KnowledgeFile:
    def __init__(
        self,
        filename: str,
        knowledge_base_name: str,
        loader_kwargs: Dict = {},
    ):
        self.kb_name = knowledge_base_name
        self.filename = str(Path(filename).as_posix())
        self.ext = os.path.splitext(filename)[-1].lower()
        if self.ext not in SUPPORTED_EXTS:
            raise ValueError(f"暂未支持的文件格式 {self.filename}")
        self.loader_kwargs = loader_kwargs
        self.filepath = get_file_path(knowledge_base_name, filename)
        self.docs = None
        self.splited_docs = None
        self.document_loader_name = get_LoaderClass(self.ext)
        self.text_splitter_name = KBSettings().TEXT_SPLITTER_NAME

    def docs2texts(
        self,
        docs: List[Document] = None,
        zh_title_enhance: bool = KBSettings().ZH_TITLE_ENHANCE,
        refresh: bool = False,
        chunk_size: int = KBSettings().CHUNK_SIZE,
        chunk_overlap: int = KBSettings().OVERLAP_SIZE,
        text_splitter: TextSplitter = None,
    ):
        docs = docs or self.file2docs(refresh=refresh)
        if not docs:
            return []
        if self.ext not in [".csv"]:
            if text_splitter is None:
                text_splitter = make_text_splitter(
                    splitter_name=self.text_splitter_name,
                    chunk_size=chunk_size,
                    chunk_overlap=chunk_overlap,
                )
            if self.text_splitter_name == "MarkdownHeaderTextSplitter":
                docs = text_splitter.split_text(docs[0].page_content)
            else:
                docs = text_splitter.split_documents(docs)

        if not docs:
            return []

        print(f"文档切分示例：{docs[0]}")
        if zh_title_enhance:
            docs = func_zh_title_enhance(docs)
        self.splited_docs = docs
        return self.splited_docs

    def file2text(
        self,
        zh_title_enhance: bool = KBSettings().ZH_TITLE_ENHANCE,
        refresh: bool = False,
        chunk_size: int = KBSettings().CHUNK_SIZE,
        chunk_overlap: int = KBSettings().OVERLAP_SIZE,
        text_splitter: TextSplitter = None,
    ):
        if self.splited_docs is None or refresh:
            docs = self.file2docs()
            self.splited_docs = self.docs2texts(
                docs=docs,
                zh_title_enhance=zh_title_enhance,
                refresh=refresh,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                text_splitter=text_splitter,
            )
        return self.splited_docs

    def file_exist(self):
        return os.path.isfile(self.filepath)

    def get_mtime(self):
        return os.path.getmtime(self.filepath)

    def get_size(self):
        return os.path.getsize(self.filepath)


def files2docs_in_thread_file2docs(
    *, file: KnowledgeFile, **kwargs
) -> Tuple[bool, Tuple[str, str, List[Document]]]:
    try:
        return True, (file.kb_name, file.filename, file.file2text(**kwargs))
    except Exception as e:
        msg = f"从文件 {file.kb_name}/{file.filename} 加载文档时出错：{e}"
        logger.error(f"{e.__class__.__name__}: {msg}")
        return False, (file.kb_name, file.filename, msg)


def files2docs_in_thread(
    files: List[Union[KnowledgeFile, Tuple[str, str], Dict]],
    chunk_size: int = KBSettings().CHUNK_SIZE,
    chunk_overlap: int = KBSettings().OVERLAP_SIZE,
    zh_title_enhance: bool = KBSettings().ZH_TITLE_ENHANCE,
) -> Generator:
    """
    利用多线程批量将磁盘文件转化成langchain Document.
    如果传入参数是Tuple，形式为(filename, kb_name)
    生成器返回值为 status, (kb_name, file_name, docs | error)
    """

    kwargs_list = []
    for i, file in enumerate(files):
        kwargs = {}
        try:
            if isinstance(file, tuple) and len(file) >= 2:
                filename = file[0]
                kb_name = file[1]
                file = KnowledgeFile(filename=filename, knowledge_base_name=kb_name)
            elif isinstance(file, dict):
                filename = file.pop("filename")
                kb_name = file.pop("kb_name")
                kwargs.update(file)
                file = KnowledgeFile(filename=filename, knowledge_base_name=kb_name)
            kwargs["file"] = file
            kwargs["chunk_size"] = chunk_size
            kwargs["chunk_overlap"] = chunk_overlap
            kwargs["zh_title_enhance"] = zh_title_enhance
            kwargs_list.append(kwargs)
        except Exception as e:
            yield False, (kb_name, filename, str(e))

    for result in run_in_thread_pool(
        func=files2docs_in_thread_file2docs, params=kwargs_list
    ):
        yield result


def format_reference(kb_name: str, docs: List[Dict], api_base_url: str="") -> List[Dict]:
    '''
    将知识库检索结果格式化为参考文档的格式
    '''
    from chatchat.server.utils import api_address
    api_base_url = api_base_url or api_address(is_public=True)

    source_documents = []
    for inum, doc in enumerate(docs):
        filename = doc.get("metadata", {}).get("source")
        parameters = urlencode(
            {
                "knowledge_base_name": kb_name,
                "file_name": filename,
            }
        )
        api_base_url = api_base_url.strip(" /")
        url = (
            f"{api_base_url}/knowledge_base/download_doc?" + parameters
        )
        page_content = doc.get("page_content")
        ref = f"""出处 [{inum + 1}] [{filename}]({url}) \n\n{page_content}\n\n"""
        source_documents.append(ref)
    
    return source_documents


if __name__ == "__main__":
    from pprint import pprint

    kb_file = KnowledgeFile(
        filename="E:\\LLM\\Data\\Test.md", knowledge_base_name="samples"
    )
    # kb_file.text_splitter_name = "RecursiveCharacterTextSplitter"
    kb_file.text_splitter_name = "MarkdownHeaderTextSplitter"
    docs = kb_file.file2docs()
    # pprint(docs[-1])
    texts = kb_file.docs2texts(docs)
    for text in texts:
        print(text)


def get_kb_path() -> str:
    """获取知识库根目录路径"""
    return KBSettings().KB_ROOT_PATH

def get_doc_path(knowledge_base_name: str) -> str:
    """获取知识库文档路径"""
    return os.path.join(get_kb_path(), knowledge_base_name)

def get_file_path(knowledge_base_name: str, filename: str) -> str:
    """获取文件在知识库中的路径"""
    return os.path.join(get_doc_path(knowledge_base_name), filename)


def list_files_from_folder(knowledge_base_name: str) -> List[str]:
    """列出知识库目录下的所有文件"""
    kb_path = get_doc_path(knowledge_base_name)
    if not os.path.exists(kb_path):
        return []
    
    files = []
    for file in os.listdir(kb_path):
        file_path = os.path.join(kb_path, file)
        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[-1].lower()
            if ext in SUPPORTED_EXTS:
                files.append(file)
    return files

def validate_kb_name(kb_name: str) -> bool:
    """
    校验知识库名称是否合法
    """
    # 检查是否为空或者只包含空格
    if not kb_name or kb_name.isspace():
        return False
        
    # 检查长度
    if len(kb_name) > 50:
        return False
        
    # 只允许中文、英文、数字、下划线和短横线
    pattern = r'^[\u4e00-\u9fa5a-zA-Z0-9_-]+$'
    if not re.match(pattern, kb_name):
        return False
        
    # 不允许的特殊名称
    reserved_names = ['tmp', 'temp', 'system', 'root', 'admin']
    if kb_name.lower() in reserved_names:
        return False
        
    return True

# 在文件末尾添加
def list_kbs_from_folder() -> List[str]:
    """列出知识库目录下的所有知识库名称"""
    kb_path = get_kb_path()
    if not os.path.exists(kb_path):
        return []
    
    kbs = []
    for kb_name in os.listdir(kb_path):
        kb_dir = os.path.join(kb_path, kb_name)
        # 只返回目录，不返回文件
        if os.path.isdir(kb_dir):
            kbs.append(kb_name)
    return kbs


def get_vs_path(knowledge_base_name: str) -> str:
    """获取向量库路径"""
    return os.path.join(get_kb_path(), knowledge_base_name, "vector_store")

LOADER_DICT = {
    "txt": "文本文件",
    "pdf": "PDF文件",
    "docx": "Word文档",
    "pptx": "PowerPoint演示文稿",
    "xlsx": "Excel表格",
    "csv": "CSV表格",
    "md": "Markdown文件",
    "json": "JSON文件",
    "html": "HTML文件"
}
