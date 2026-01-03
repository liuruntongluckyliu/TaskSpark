import streamlit as st

st.title("🎉 Streamlit安装成功！")
st.success("恭喜！现在可以开始TaskSpark项目了！")
st.write("这是一个简单的测试页面")

name = st.text_input("输入你的名字")
if name:
    st.write(f"你好，{name}！")

if st.button("点击测试"):
    st.balloons()
    st.write("🎯 一切正常！")