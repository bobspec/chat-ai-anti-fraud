import streamlit as st
import logging
# 模型下载
# from modelscope import AutoTokenizer, AutoModelForCausalLM,snapshot_download
# from modelscope import snapshot_download
from modelscope.hub.snapshot_download import snapshot_download
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

# 创建一个标题和一个副标题
st.title("💬 InternLM2-Chat-7B 防诈骗专家")
st.caption("🚀 A streamlit chatbot powered by InternLM2 QLora")

try:
    logging.debug("Starting model download...")
    model_dir = snapshot_download('Shanghai_AI_Laboratory/internlm2-chat-1_8b', revision='v1.1.0')
    logging.debug(f"Model downloaded to {model_dir}")
except Exception as e:
    logging.error(f"Error during model download: {e}")
    st.error(f"Error during model download: {e}")


# 定义一个函数，用于获取模型和tokenizer
@st.cache_resource
def get_model():
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


tokenizer, model = get_model()

if tokenizer is None or model is None:
    st.stop()  # 停止运行，如果模型加载失败

with st.sidebar:
    st.markdown("## InternLM LLM")
    st.markdown("[InternLM](https://github.com/InternLM/InternLM.git)")
    st.markdown("[ChatAI反诈骗](https://gitee.com/xiangboit/chat-ai-anti-fraud)")
    max_length = st.slider("max_length", 0, 1024, 512, step=1)
    system_prompt = st.text_input("System_Prompt",
                                  "现在你要扮演防诈骗专家并且和用户进行聊天，要求用户提供相关的信息，根据用户提供的信息判定用户是否遭受了诈骗并给出后续建议")

if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state.messages:
    st.chat_message("user").write(msg[0])
    st.chat_message("assistant").write(msg[1])

if prompt := st.chat_input():
    st.chat_message("user").write(prompt)
    try:
        logging.info(f"User input received: {prompt}")

        # 拼接系统提示词和用户输入
        full_prompt = f"{system_prompt}\n{prompt}"

        response, history = model.chat(tokenizer, full_prompt, history=st.session_state.messages)
        logging.info(f"Model response generated: {response}")

        st.session_state.messages.append((prompt, response))
        st.chat_message("assistant").write(response)
    except Exception as e:
        logging.error(f"Error during model response generation: {e}")
        st.error(f"Error during model response generation: {e}")