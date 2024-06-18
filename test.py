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


@st.cache_resource
def get_model(model_dir):
    try:
        logging.debug("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
        logging.debug("Tokenizer loaded successfully")

        logging.debug("Loading model...")
        if torch.cuda.is_available():
            device = torch.device("cuda")
            logging.debug("Using GPU for model loading")
            model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.float16)
        else:
            device = torch.device("cpu")
            logging.debug("Using CPU for model loading")
            model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.float32)
        model = model.to(device)
        model = model.eval()
        logging.debug("Model loaded successfully")
        return tokenizer, model
    except Exception as e:
        logging.error(f"Error during model loading: {e}")
        st.error(f"Error during model loading: {e}")
        return None, None


def setup_sidebar():
    st.sidebar.title("InternLM LLM")
    st.sidebar.markdown("[InternLM](https://github.com/InternLM/InternLM.git)")
    st.sidebar.markdown("[ChatAI反诈骗](https://gitee.com/xiangboit/chat-ai-anti-fraud)")

    st.session_state.system_prompt = st.sidebar.text_input("System_Prompt",
                                                           "现在你要扮演防诈骗专家并且和用户进行聊天，要求用户提供相关的信息，根据用户提供的信息判定用户是否遭受了诈骗并给出后续建议")

    st.sidebar.markdown("## 输入案例内容")
    if 'input_text' not in st.session_state:
        st.session_state.input_text = ""

    st.session_state.user_input = st.sidebar.text_area(
        "",
        height=300,
        placeholder="请输入案例内容",
        key="input_text",
        label_visibility='visible',
        help="在此输入案例内容"
    )

    st.sidebar.markdown("## 上传相关图片")
    if 'uploaded_files' not in st.session_state:
        st.session_state.uploaded_files = []

    uploaded_files = st.sidebar.file_uploader(
        "",
        type=['jpg', 'jpeg', 'png'],
        accept_multiple_files=True,
        label_visibility='visible',
        help="上传相关图片以辅助分析"
    )
    if uploaded_files:
        st.session_state.uploaded_files = uploaded_files

    st.sidebar.markdown("## 控制显示选项")
    if 'show_image_analysis' not in st.session_state:
        st.session_state.show_image_analysis = False

    st.session_state.show_image_analysis = st.sidebar.checkbox(
        "显示图片解析结果",
        value=st.session_state.show_image_analysis,
        help="开启后显示所选择的图片及其文本描述"
    )


def process_with_tencent_ocr(images, secret_id, secret_key):
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

        return {'ocr_results': ocr_results}

    except TencentCloudSDKException as err:
        logging.error(f"Tencent Cloud SDK Exception: {err}")
        return {'error': err, 'ocr_results': []}


def analyze_text(text, ocr_results):
    """
    对输入的文本进行分析。
    Args:
        text (str): 用户输入的文本。
    Returns:
        str: 分析结果。
    """
    try:
        logging.debug("Starting model download...")
        model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-1_8b', revision='v1.1.0')
        logging.debug(f"Model downloaded to {model_dir}")
    except Exception as e:
        logging.error(f"Error during model download: {e}")
        st.error(f"Error during model download: {e}")
        model_dir = None

    if model_dir:
        tokenizer, model = get_model(model_dir)
    else:
        tokenizer, model = None, None

    if tokenizer is None or model is None:
        return "模型加载失败"
    ocr_texts = "\n".join([res["text"] for res in ocr_results])
    full_prompt = f"案例描述：\n{text}\n相关聊天记录：\n{ocr_texts}"
    logging.info(f"full_prompt message: {full_prompt}")
    response, history = model.chat(tokenizer, full_prompt, meta_instruction=st.session_state.system_prompt)
    logging.info(f"mode response: {response}")
    return {'result': response}


def display_results(result, analysis_result):
    """
    显示解析结果和图片选择器。
    Args:
        result (dict): OCR处理结果。
        analysis_result (str): 文本分析结果。
    """
    st.markdown("### 解析结果")
    st.markdown(analysis_result.get('result', 'No result returned'))

    if result.get('ocr_results'):
        st.markdown("### 图片内容")
        selected_image = image_select(
            label="图片列表",
            images=[Image.open(res['image']) for res in result['ocr_results']],
            captions=[f"图片{idx + 1}" for idx in range(len(result['ocr_results']))],
            use_container_width=True,
            return_value="original",
            key="image_select"
        )

        if selected_image != st.session_state.get('selected_image'):
            st.session_state.selected_image = selected_image
        if st.session_state.show_image_analysis:
            if 'selected_image' in st.session_state and st.session_state.selected_image:
                for res in result['ocr_results']:
                    image = Image.open(res['image'])
                    if image == st.session_state.selected_image:
                        st.image(image, caption="选中的图片", use_column_width=True)
                        st.markdown(res['text'])
                        break


def main():
    st.title("案例分析展示")
    st.caption("使用模型进行案例分析")
    setup_sidebar()

    if st.sidebar.button('提交', key='submit_button', help="点击提交"):
        if st.session_state.user_input or st.session_state.uploaded_files:
            secret_id = 'x'
            secret_key = 'x'

            with st.spinner('正在处理中，请稍候...'):
                result = process_with_tencent_ocr(st.session_state.uploaded_files,
                                                  secret_id, secret_key)
                logging.info(result)
                analysis_result = analyze_text(st.session_state.user_input, result['ocr_results'])

            if 'error' in result:
                st.error(result['error'])
            else:
                st.session_state.result = result
                st.session_state.analysis_result = analysis_result
                # 清除之前选中的图片，避免干扰
                st.session_state.selected_image = None
                st.session_state.display_result = True

    if 'analysis_result' in st.session_state and st.session_state.analysis_result:
        display_results(st.session_state.result, st.session_state.analysis_result)


if __name__ == "__main__":
    main()
