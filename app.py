import streamlit as st

introduce = st.Page("./pages/introduce.py", title="主页", icon=":material/house:")
ai_assistant = st.Page("./pages/ai_assistant.py", title="AI 小助手", icon=":material/nephrology:")
ai_report = st.Page("./pages/ai_report.py", title="案情分析", icon=":material/electric_bolt:")


pg = st.navigation([introduce, ai_assistant,ai_report])
st.set_page_config(page_title="Ai 反诈", page_icon=":material/edit:")
pg.run()
