import streamlit as st
import logging
from streamlit_image_select import image_select
from PIL import Image
import io
import base64
import json
import time
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.ocr.v20181119 import ocr_client, models

# 创建一个标题和一个副标题
st.title("案例分析展示")
st.caption("使用模型进行案例分析，并以优雅布局展示结果")

# 左侧侧边栏布局，放置文本输入框
st.sidebar.markdown("## 输入案例内容")
if 'input_text' not in st.session_state:
    st.session_state.input_text = ""

user_input = st.sidebar.text_area(
    "请输入案例内容",
    height=300,
    placeholder="请输入案例内容",
    key="input_text",
    label_visibility='visible',
    help="在此输入案例内容"
)

# 右侧侧边栏布局，放置文件上传
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []

st.sidebar.markdown("## 上传相关图片")
uploaded_files = st.sidebar.file_uploader(
    "上传相关图片",
    type=['jpg', 'jpeg', 'png'],
    accept_multiple_files=True,
    label_visibility='visible',
    help="上传相关图片以辅助分析"
)
if uploaded_files:
    st.session_state.uploaded_files = uploaded_files


def process_with_tencent_ocr(text, images, secret_id, secret_key):
    """
    使用腾讯云OCR服务处理图像。
    Args:
        text (str): 用户输入的文本。
        images (list): 用户上传的图像文件列表。
        secret_id (str): 腾讯云API密钥ID。
        secret_key (str): 腾讯云API密钥。
    Returns:
        dict: 包含处理结果的字典，如果请求失败，则返回错误信息。
    """
    try:
        cred = credential.Credential(secret_id, secret_key)
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        # 处理每张图片
        ocr_results = []
        for idx, file in enumerate(images):
            image = Image.open(file)
            buffered = io.BytesIO()
            image.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            req = models.GeneralBasicOCRRequest()
            params = {
                "ImageBase64": img_str
            }
            req.from_json_string(json.dumps(params))
            resp = client.GeneralBasicOCR(req)
            result = json.loads(resp.to_json_string())

            text_detected = "\n".join([item["DetectedText"] for item in result["TextDetections"]])
            ocr_results.append({
                "image": file,
                "text": f"图片{idx + 1}识别内容:\n{text_detected}\n"
            })

        return {'result': text, 'ocr_results': ocr_results}

    except TencentCloudSDKException as err:
        logging.error(f"Tencent Cloud SDK Exception: {err}")
        return {'error': f"Tencent Cloud SDK Exception: {err}"}


# 提交按钮
if st.sidebar.button('提交', key='submit_button', help="点击提交"):
    if user_input or uploaded_files:
        secret_id = 'x'  # 替换为你的腾讯云Secret ID
        secret_key = 'x'  # 替换为你的腾讯云Secret Key

        with st.spinner('正在处理中，请稍候...'):
            time.sleep(10)
            result = process_with_tencent_ocr(user_input, uploaded_files, secret_id, secret_key)

        if 'error' in result:
            st.error(result['error'])
            if 'details' in result:
                st.error(result['details'])
        else:
            st.session_state.result = result
            st.session_state.selected_image = None  # 清除之前选中的图片，避免干扰
            st.session_state.display_result = True

# 显示解析结果和图片选择器
if 'result' in st.session_state and st.session_state.result:
    st.markdown("### 解析结果")
    st.markdown(st.session_state.result.get('result', 'No result returned'))

    if st.session_state.result.get('ocr_results'):
        st.markdown("### 图片及其识别内容")
        selected_image = image_select(
            label="选择一张图片查看",
            images=[Image.open(res['image']) for res in st.session_state.result['ocr_results']],
            captions=[f"图片{idx + 1}" for idx in range(len(st.session_state.result['ocr_results']))],
            use_container_width=True,
            return_value="original",
            key="image_select"
        )

        # 更新选中的图片
        if selected_image != st.session_state.get('selected_image'):
            st.session_state.selected_image = selected_image

        # 展示选中的图片及其识别内容
        if 'selected_image' in st.session_state and st.session_state.selected_image:
            for res in st.session_state.result['ocr_results']:
                image = Image.open(res['image'])
                if image == st.session_state.selected_image:
                    st.image(image, caption="选中的图片", use_column_width=True)
                    st.markdown(res['text'])
                    break
