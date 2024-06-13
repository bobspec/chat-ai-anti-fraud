import streamlit as st
import logging
from modelscope.hub.snapshot_download import snapshot_download
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from streamlit_image_select import image_select
from PIL import Image
# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 创建一个标题和一个副标题
st.title("案例分析展示")
st.caption("使用模型进行案例分析，并以优雅布局展示结果")
# try:
#     logging.debug("Starting model download...")
#     model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-7b', revision='v1.1.0')
#     logging.debug(f"Model downloaded to {model_dir}")
# except Exception as e:
#     logging.error(f"Error during model download: {e}")
#     st.error(f"Error during model download: {e}")


# # 定义一个函数，用于获取模型和tokenizer
# @st.cache_resource
# def get_model():
#     try:
#         logging.debug("Loading tokenizer...")
#         tokenizer = AutoTokenizer.from_pretrained(model_dir, trust_remote_code=True)
#         logging.debug("Tokenizer loaded successfully")
#
#         logging.debug("Loading model...")
#         if torch.cuda.is_available():
#             device = torch.device("cuda")
#             logging.debug("Using GPU for model loading")
#             model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.float16)
#         else:
#             device = torch.device("cpu")
#             logging.debug("Using CPU for model loading")
#             model = AutoModelForCausalLM.from_pretrained(model_dir, trust_remote_code=True, torch_dtype=torch.float32)
#
#         model = model.to(device)
#         model = model.eval()
#         logging.debug("Model loaded successfully")
#         return tokenizer, model
#     except Exception as e:
#         logging.error(f"Error during model loading: {e}")
#         st.error(f"Error during model loading: {e}")
#         return None, None
#
#
# tokenizer, model = get_model()
#
# if tokenizer is None or model is None:
#     st.stop()  # 停止运行，如果模型加载失败

# 中间布局的输入框和文件上传
st.markdown("""
    <style>
        .center-form {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
        }
        .custom-text-area {
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 0.25rem;
        }
        .custom-file-uploader {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 100%;
            padding: 0.5rem;
            border: 1px solid #ccc;
            border-radius: 0.25rem;
            background-color: #f9f9f9;
            cursor: pointer;
            margin-top: 0.5rem;
        }
        .custom-submit-button {
            width: 100%;
            padding: 0.5rem;
            border: none;
            border-radius: 0.25rem;
            background-color: #007bff;
            color: white;
            font-size: 1rem;
            cursor: pointer;
            margin-top: 0.5rem;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("<div class='center-form'>", unsafe_allow_html=True)

# 使用一个表单将文件上传和文本输入框融合在一起
with st.form(key='input_form'):
    user_input = st.text_area("请输入案例内容", height=100, label_visibility='collapsed', placeholder="请输入案例内容")
    uploaded_files = st.file_uploader("上传相关图片", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True,
                                      label_visibility='collapsed')

    submit_button = st.form_submit_button(label='提交', help="点击提交")


gallery_placeholder = st.empty()

# 解析案例并显示结果
if submit_button:
    if user_input:
        st.markdown("### 解析结果")
        try:
            # 模型处理，这里简单示意，实际应用中需要根据模型的具体功能来拆解案例
            reasons = ["原因: 这里是原因1", "原因: 这里是原因2"]
            backgrounds = ["背景: 这里是背景1", "背景: 这里是背景2"]
            contents = ["内容: 这里是内容1", "内容: 这里是内容2"]
            user_infos = ["用户信息: 这里是用户信息1", "用户信息: 这里是用户信息2"]

            # 合并所有解析结果并显示为Markdown
            results = reasons + backgrounds + contents + user_infos
            markdown_text = "\n\n".join(results)
            st.markdown(markdown_text)

        except Exception as e:
            logging.error(f"Error during model processing: {e}")
            st.error(f"Error during model processing: {e}")
    with gallery_placeholder.container():
        if uploaded_files:
            st.markdown("### 上传的图片")
            images = []
            captions = []
            for file in uploaded_files:
                image = Image.open(file)
                if image.mode == 'RGBA':
                    image = image.convert('RGB')
                images.append(image)
                captions.append(file.name)

            selected_image = image_select(
                label="选择一张图片查看",
                images=images,
                captions=captions,
                use_container_width=True,
                return_value="original"
            )
            # if selected_image:
            #     st.image(selected_image, caption="选中的图片", use_column_width=True)
st.markdown("</div>", unsafe_allow_html=True)
