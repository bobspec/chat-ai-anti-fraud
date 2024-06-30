import streamlit as st


st.write("### 欢迎来到 反诈助手!!! 👋👋👋")
st.markdown("项目GitHub链接 [ChatAI反诈骗](https://github.com/bobspec/chat-ai-anti-fraud.git)")

# 显示Logo和标题居中
st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://raw.githubusercontent.com/bobspec/chat-ai-anti-fraud/main/image/logo.png" width="200"/>
        <div>
            <b><font size="5">Chat-反诈</font></b>
        </div>
    </div>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    
    ### 背景介绍
    反诈模型的开发源于我们观察到遭受到诈骗的人群越来越趋向于青少年，而诈骗手段层出不穷，很多人因缺乏防范意识和应对技巧，轻易成为诈骗分子的目标，蒙受巨大的财产损失和精神伤害。尽管社会各界不断加强反诈提示和宣传，帮助人们提高警惕，但依然有大量人群未能及时辨别出诈骗陷阱。
    我们决定利用人工智能技术，开发一个智能反诈助手。反诈模型通过学习大量的诈骗案例和对话数据，能够在用户与潜在诈骗者的对话中实时提供预警和建议，帮助用户迅速识别和应对诈骗行为。我们的目标是将这些智能防范手段普及到更多人群，尤其是那些不太了解网络安全的用户，从而有效减少诈骗事件的发生
    
    ####  已完成功能
    * 反诈骗模型1.8B训练及评测
    * 功能一 AI反诈助手
    * 功能二 AI案情鉴定分析
    
    #### TODO
    * 数据集变更相关【】格式为markdown格式
    * 优化AI案情鉴定展示效果
    * AI生成宣传图片
    * Ai生成宣称视频
    * Ai反诈骗意识训练游戏
    """
)

# 显示AI反诈骗图片
st.markdown("#### AI反诈骗")
st.image("./image/ai_assistant.png")
st.markdown("描述: AI反诈助手能够通过对话分析，实时提供诈骗预警和建议。")

# 显示AI案情鉴定分析图片
st.markdown("#### AI案情鉴定分析")
st.image("./image/ai_report.png")
st.markdown("描述: AI案情鉴定分析能够通过对话分析，提供详细的案情报告。")

