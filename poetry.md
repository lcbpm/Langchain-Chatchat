### 刷新libs
poetry add ./libs/chatchat-server/

pip install -e  ./libs/chatchat-server

-e 参数代表 "editable" 或 "develop" 模式安装，它有以下特点：
可编辑模式：
不会将代码复制到 Python 的 site-packages 目录
而是在 site-packages 中创建一个链接，指向你的源代码位置
当你修改源代码时，不需要重新安装包，修改会直接生效
开发友好：
特别适合开发阶段使用
可以直接修改源码并测试效果
不用反复运行 pip install 命令

把项目源代码安装成包，直接调试，路径下面需要有这两种配置
（setup.py 或 pyproject.toml）