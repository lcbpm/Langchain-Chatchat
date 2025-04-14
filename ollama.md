### ollama
brew install ollama
ollama serve
### 下载嵌入模型
ollama pull nomic-embed-text

### 下载对话模型
ollama pull llama3

### 使用模型对话
ollama run llama3

# 停止当前运行的 Ollama 服务
pkill ollama



# 多次使用 deactivate 命令直到提示符恢复正常
deactivate
deactivate

# 如果上面的命令不足以退出所有环境，可以使用以下命令
while [ -n "$VIRTUAL_ENV" ]; do deactivate; done

# cli.py
poetry run python cli.py init
poetry run python cli.py kb -r


# 首先确保已退出所有环境
deactivate  # 可能需要执行多次

# 第一次激活
source .venv/bin/activate

# 第二次激活同一环境
source .venv/bin/activate