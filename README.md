# ani-strm

# 一、环境检查与依赖安装
Python 3 安装与验证：多数 Linux 发行版默认 Python 版本可能有别，需确保 Python 3 正确安装并设为默认。如在 Ubuntu 或 Debian 中，可执行 sudo apt-get update && sudo apt-get install python3 安装，再用 python3 --version 验证。CentOS 或 RHEL 则用 yum install python3 安装并检查版本。
依赖库确认与安装：脚本依赖库通常在 Python 3 标准库中，但部分发行版可能需额外安装或更新。可在脚本开头加依赖检查代码段，如 import importlib.util; spec = importlib.util.find_spec('urllib.parse'); if spec is None: print("urllib.parse 模块缺失，请安装相应库"); exit(1)，依提示用包管理器解决依赖问题，如 pip3 install --upgrade urllib。
# 二、脚本权限设置与执行
文件权限调整：赋予脚本执行权限，在终端进入脚本所在目录，执行 chmod +x strm.py，使所有者、组及其他用户有执行权，方便从任何目录运行脚本，命令为 ./strm.py。
路径配置（若有需要）：若脚本运行依赖特定路径下的文件或目录，确保在不同 Linux 系统中路径设置正确且存在。可在脚本开头用 os.path.exists 检查关键路径，不存在则提示用户创建或调整路径，如 if not os.path.exists('/path/to/required/directory'): print("关键目录不存在，请创建并确保权限正确"); exit(1)。
