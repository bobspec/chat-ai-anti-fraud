import os
import subprocess

# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 安装依赖包
requirements_path = os.path.join(current_dir, 'requirements.txt')
install_result = subprocess.run(['pip', 'install', '-r', requirements_path])

# 运行 Streamlit 应用
app_path = os.path.join(current_dir, 'test.py')
print(f"App path: {app_path}")
run_result = subprocess.run(['streamlit', 'run', app_path, '--server.address=127.0.0.1', '--server.port', '7860',"--logger.level","debug"])
print(f"Run result: {run_result}")