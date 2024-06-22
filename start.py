import logging
import os
import subprocess

import streamlit as st
from modelscope.hub.snapshot_download import snapshot_download

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    logging.debug("Starting model download...")
    model_dir = snapshot_download('EricSC/Fanzha1_8B', revision='v1.0.0')
    logging.debug(f"Model downloaded to {model_dir}")
except Exception as e:
    logging.error(f"Error during model download: {e}")
    st.error(f"Error during model download: {e}")
    model_dir = None

# 安装依赖包
requirements_path = os.path.join(current_dir, 'requirements.txt')
install_result = subprocess.run(['pip', 'install', '-r', requirements_path])

# 运行 Streamlit 应用
app_path = os.path.join(current_dir, 'app.py')
print(f"App path: {app_path}")
run_result = subprocess.run(['streamlit', 'run', app_path, '--server.address=127.0.0.1', '--server.port', '7860',"--logger.level","debug"])
print(f"Run result: {run_result}")