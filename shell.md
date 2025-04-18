# 添加到您的 shell 配置文件
function activate_venv() {
    # 退出所有可能的环境
    deactivate 2>/dev/null || true
    conda deactivate 2>/dev/null || true
    
    # 激活指定的 venv
    source "$1/bin/activate"
}

function activate_conda() {
    # 退出所有可能的环境
    deactivate 2>/dev/null || true
    conda deactivate 2>/dev/null || true
    
    # 激活指定的 conda 环境
    conda activate "$1"
}


# 激活 .venv
activate_venv .venv

# 激活 conda 环境
activate_conda base

### 更新
pip install -e .
poetry install
### 刷新libs
poetry add ./libs/chatchat-server/


# 创建虚拟环境
python -m venv myenv

# 激活虚拟环境
# Windows
myenv\Scripts\activate
# Linux/macOS
source myenv/bin/activate

# 退出虚拟环境
deactivate


pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
pip config set global.extra-index-url "https://mirrors.aliyun.com/pypi/simple/ https://pypi.mirrors.ustc.edu.cn/simple/ https://repo.huaweicloud.com/repository/pypi/simple https://pypi.doubanio.com/simple/"
pip config set global.trusted-host "pypi.tuna.tsinghua.edu.cn mirrors.aliyun.com pypi.mirrors.ustc.edu.cn repo.huaweicloud.com pypi.doubanio.com"

# 基本卸载命令
pip uninstall -y jiter

# 确保以正确的架构模式运行（如果在 ARM64 Mac 上）
arch -arm64 pip uninstall -y jiter

arch -arm64 pip install jiter


# 以 arm64 模式安装 python 包
arch -arm64 pip install numpy

# 以 x86_64 模式运行程序
arch -x86_64 python script.py

清理缓存
pip cache purge

pip install git+https://github.com/aio-libs/frozenlist.git
pip install 本地路径