import streamlit as st
import logging
from streamlit_image_select import image_select
from PIL import Image
import io
import requests
import time

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

def process_with_openai(text, images, api_endpoint, api_key):
    """
    使用OpenAI处理文本和图像的函数。

    Args:
        text (str): 用户输入的文本。
        images (list): 用户上传的图像文件列表。
        api_endpoint (str): OpenAI API端点。
        api_key (str): OpenAI API密钥。

    Returns:
        dict: 包含处理结果的字典，如果请求失败，则返回错误信息。
    """
    try:
        # # 准备数据
        # data = {
        #     'text': text,
        # }
        # files = []
        # for idx, file in enumerate(images):
        #     image = Image.open(file)
        #     if image.mode == 'RGBA':
        #         image = image.convert('RGB')
        #     buf = io.BytesIO()
        #     image.save(buf, format='JPEG')
        #     buf.seek(0)
        #     files.append(('images', (f'image_{idx}.jpg', buf, 'image/jpeg')))
        #
        # # 发送请求到OpenAI API
        # response = requests.post(
        #     api_endpoint,
        #     data=data,
        #     files=files,
        #     headers={'Authorization': f'Bearer {api_key}'}
        # )

        # if response.status_code == 200:
        #     return response.json()
        # else:
        #     return {'error': f"Error: {response.status_code}", 'details': response.text}
        return {'result':"案例分析\n" +
                "案例叙述\n" +
                "在一个快速发展的科技公司，名为TechInnovate，拥有300多名员工，专注于人工智能和大数据分析的研发与应用。公司内部设有多个项目组，每个项目组由不同领域的专家组成，负责不同的创新项目。然而，随着公司规模的扩大和项目数量的增加，内部沟通和协作变得越来越困难。项目组之间的信息不对称和资源分配不均问题逐渐显现，导致一些项目进展缓慢，甚至出现失败的情况。为了应对这些挑战，TechInnovate决定引入一套新的项目管理系统，希望通过优化内部沟通和资源分配，提高整体工作效率和项目成功率。\n" +
                "\n" +
                "背景分析\n" +
                "TechInnovate成立于2010年，起初是一家小型创业公司，专注于人工智能算法的研究和开发。随着技术的不断突破和市场需求的增加，公司逐渐扩大规模，吸引了大量的技术人才和投资。在此过程中，公司项目数量迅速增加，各项目组也逐步形成独立的工作团队。然而，随着公司规模的扩大，原有的项目管理模式逐渐暴露出一些问题：\n" +
                "\n" +
                "信息不对称：各项目组之间缺乏有效的信息共享机制，导致重复劳动和资源浪费。\n" +
                "资源分配不均：由于缺乏统一的资源管理平台，一些项目组资源过剩，而另一些项目组则资源匮乏，影响了项目的正常推进。\n" +
                "沟通效率低下：跨部门沟通不畅，导致决策流程缓慢，影响了项目的及时调整和优化。\n" +
                "为了解决上述问题，公司决定引入一套新的项目管理系统，以实现以下目标：\n" +
                "\n" +
                "提高内部沟通效率，建立有效的信息共享机制。\n" +
                "优化资源分配，确保各项目组资源的合理配置。\n" +
                "提高项目管理的透明度，促进跨部门的协作与决策。\n" +
                "内容分析\n" +
                "新的项目管理系统主要包括以下几个模块：\n" +
                "\n" +
                "信息共享平台：该平台旨在打破项目组之间的信息壁垒，通过集中化的信息发布和共享机制，使各项目组能够及时获取其他组的最新动态和资源信息，避免重复劳动和资源浪费。\n" +
                "\n" +
                "资源管理系统：该系统提供统一的资源登记、分配和调度功能，确保各项目组能够根据项目需求合理分配和使用公司资源。通过实时监控和分析，各项目组可以及时调整资源配置，提高资源利用效率。\n" +
                "\n" +
                "沟通协作工具：引入即时通讯、视频会议和任务管理等工具，方便跨部门的沟通和协作。该工具还支持会议纪要和任务分配功能，确保各项工作有序推进。\n" +
                "\n" +
                "项目监控与分析：该模块提供项目进度监控、风险管理和绩效分析等功能，通过数据分析和可视化工具，管理层可以实时掌握各项目的进展情况，及时发现并解决潜在问题。\n" +
                "\n" +
                "通过引入这套新的项目管理系统，TechInnovate期望能够解决目前存在的内部沟通和资源分配问题，提升整体工作效率和项目成功率。系统实施后，公司内部的协作与沟通得到了显著改善，项目进度加快，资源利用率提高，进一步巩固了TechInnovate在人工智能和大数据领域的领先地位。"}

    except Exception as e:
        logging.error(f"Error during model processing: {e}")
        return {'error': f"Error during model processing: {e}"}


# 提交按钮
if st.sidebar.button('提交', key='submit_button', help="点击提交"):
    if user_input or uploaded_files:
        api_endpoint = 'YOUR_OPENAI_API_ENDPOINT'  # 替换为你的OpenAI API端点
        api_key = 'YOUR_API_KEY'  # 替换为你的API密钥

        with st.spinner('正在处理中，请稍候...'):
            time.sleep(10)
            st.markdown("### 解析结果")
            result = process_with_openai(user_input, uploaded_files, api_endpoint, api_key)

        if 'error' in result:
            st.error(result['error'])
            if 'details' in result:
                st.error(result['details'])
        else:
            st.markdown(result.get('result', 'No result returned'))

        # 展示上传的图片
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
            if selected_image:
                st.image(selected_image, caption="选中的图片", use_column_width=True)

    else:
        st.error("请输入案例内容或上传相关图片")
