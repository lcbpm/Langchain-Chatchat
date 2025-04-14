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