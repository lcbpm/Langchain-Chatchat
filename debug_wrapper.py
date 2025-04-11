#!/usr/bin/env python3
# debug_wrapper.py

import os
import sys
import subprocess

# 打印当前环境信息
print(f"Python解释器: {sys.executable}")
print(f"Python架构: {sys.platform}_{os.uname().machine}")

# 获取Poetry Python路径
poetry_python = subprocess.check_output(["poetry", "run", "which", "python"], 
                                        text=True).strip()
print(f"Poetry Python路径: {poetry_python}")

# 确保使用Poetry的Python启动目标脚本
target_script = os.path.join(os.getcwd(), 
                             "libs/chatchat-server/chatchat/server/api_server/server_app.py")

# 使用subprocess启动与poetry run等效的命令
# 在启动前设置断点
print("准备启动调试...")
breakpoint()  # 这里会进入pdb调试器

# 继续执行后将启动目标脚本
os.execv(poetry_python, [poetry_python, target_script])