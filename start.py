import os
import subprocess
import streamlit as st
import logging
from streamlit_image_select import image_select
from PIL import Image
import io
import base64
import json
import time
from modelscope.hub.snapshot_download import snapshot_download
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)
# 获取当前工作目录
current_dir = os.path.dirname(os.path.abspath(__file__))
try:
    logging.debug("Starting model download...")
    model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-1_8b', revision='v1.1.0')
    logging.debug(f"Model downloaded to {model_dir}")
except Exception as e:
    logging.error(f"Error during model download: {e}")
    st.error(f"Error during model download: {e}")
    model_dir = None

# 安装依赖包
requirements_path = os.path.join(current_dir, 'requirements.txt')
install_result = subprocess.run(['pip', 'install', '-r', requirements_path])

# 运行 Streamlit 应用
app_path = os.path.join(current_dir, 'test.py')
print(f"App path: {app_path}")
run_result = subprocess.run(['streamlit', 'run', app_path, '--server.address=127.0.0.1', '--server.port', '7860',"--logger.level","debug"])
print(f"Run result: {run_result}")