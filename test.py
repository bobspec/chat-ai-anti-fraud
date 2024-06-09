import streamlit as st
import logging
# 模型下载
from modelscope import AutoTokenizer, AutoModelForCausalLM, snapshot_download
import torch

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 创建一个标题和一个副标题
st.title("💬 InternLM2-Chat-7B 防诈骗专家")
st.caption("🚀 A streamlit chatbot powered by InternLM2 QLora")

try:
    logging.debug("Starting model download...")
    model_dir = snapshot_download("Shanghai_AI_Laboratory/internlm2-20b",revision='v1.1.0')
    logging.debug(f"Model downloaded to {model_dir}")
except Exception as e:
    logging.error(f"Error during model download: {e}")
    st.error(f"Error during model download: {e}")

# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
    try:
        logging.debug("Loading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(model_dir, device_map="auto", trust_remote_code=True)
        logging.debug("Tokenizer loaded successfully")

        logging.debug("Loading model...")
        model = AutoModelForCausalLM.from_pretrained(model_dir, device_map="auto", trust_remote_code=True, torch_dtype=torch.float16,offload_folder="/path/to/offload/folder")
        model = model.eval()
        logging.debug("Model loaded successfully")
        return tokenizer, model
    except Exception as e:
        logging.error(f"Error during model loading: {e}")
        st.error(f"Error during model loading: {e}")
        return None, None

tokenizer, model = get_model()

if tokenizer is None or model is None:
    st.stop()  # 停止运行，如果模型加载失败

with st.sidebar:
    st.markdown("## InternLM LLM")
    "[InternLM](https://github.com/InternLM/InternLM.git)"
    "[ChatAI反诈骗](https://gitee.com/xiangboit/chat-ai-anti-fraud)"
    # 创建一个滑块，用于选择最大长度，范围在0到1024之间，默认值为512
    max_length = st.slider("max_length", 0, 1024, 512, step=1)
    system_prompt = st.text_input("System_Prompt", "现在你要扮演防诈骗专家并且和用户进行聊天，要求用户提供相关的信息，根据用户提供的信息判定用户是否遭受了诈骗并给出后续建议")

# 如果session_state中没有"messages"，则创建一个包含默认消息的列表
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 遍历session_state中的所有消息，并显示在聊天界面上
for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])

# 如果用户在聊天输入框中输入了内容，则执行以下操作
if prompt := st.chat_input():
    # 在聊天界面上显示用户的输入
    st.chat_message("user").write(prompt)
    try:
        # 构建输入
        logging.info(f"User input received: {prompt}")
        response, history = model.chat(tokenizer, prompt, meta_instruction=system_prompt, history=st.session_state.messages)
        # 将模型的输出添加到session_state中的messages列表中
        st.session_state.messages.append((prompt, response))
        # 在聊天界面上显示模型的输出
        st.chat_message("assistant").write(response)
        logging.info(f"Model response generated and displayed: {response}")
    except Exception as e:
        logging.info(f"Error during model response generation: {e}")
        st.error(f"Error during model response generation: {e}")
