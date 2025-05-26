import streamlit as st
import webbrowser

# 设置页面标题和布局
st.set_page_config(page_title="VIP视频破解工具", layout="centered")

# 页面标题
st.title("🎥 VIP视频破解工具")
st.markdown("author：mengxian")
# 输入框
video_url = st.text_input("请输入网页视频链接：", placeholder="在此输入视频链接...")

# 按钮功能
def open_video(video_url):
    if video_url:
        base_url = "https://jx.xmflv.cc/?url="
        full_url = base_url + video_url
        webbrowser.open(full_url)
        st.success("正在打开VIP视频，请稍候...")
    else:
        st.error("请输入有效的视频链接！")

# 按钮操作
if st.button("播放VIP视频"):
    open_video(video_url)

# 快捷链接
st.markdown("### 快捷访问平台")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("爱奇艺"):
        webbrowser.open("https://www.iqiyi.com")

with col2:
    if st.button("腾讯视频"):
        webbrowser.open("https://v.qq.com")

with col3:
    if st.button("优酷视频"):
        webbrowser.open("https://www.youku.com/")

# 提示信息
st.info("提示：将视频链接复制到输入框内，点击播放VIP视频按钮即可播放。")
