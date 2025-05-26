import streamlit as st

# 设置页面标题和布局
st.set_page_config(page_title="VIP视频破解工具", layout="centered")

# 页面标题
st.title("🎥 VIP视频破解工具")
st.markdown("author：mengxian")

# 输入框
video_url = st.text_input("请输入网页视频链接：", placeholder="在此输入视频链接...")

# 按钮功能
def generate_embed_url(video_url):
    if video_url:
        base_url = "https://jx.xmflv.cc/?url="
        return base_url + video_url
    return None

# 嵌入播放器
if st.button("播放VIP视频"):
    embed_url = generate_embed_url(video_url)
    if embed_url:
        st.success("正在加载VIP视频，请稍候...")
        st.components.v1.html(
            f"""
            <iframe src="{embed_url}" width="700" height="450" frameborder="0" allowfullscreen></iframe>
            """,
            height=500,
        )
    else:
        st.error("请输入有效的视频链接！")

# 快捷链接
st.markdown("### 快捷访问平台")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("爱奇艺"):
        st.components.v1.html(
            '<iframe src="https://www.iqiyi.com" width="800" height="450" frameborder="0"></iframe>',
            height=500,
        )

with col2:
    if st.button("腾讯视频"):
        st.components.v1.html(
            '<iframe src="https://v.qq.com" width="800" height="450" frameborder="0"></iframe>',
            height=500,
        )

with col3:
    if st.button("优酷视频"):
        st.components.v1.html(
            '<iframe src="https://www.youku.com" width="800" height="450" frameborder="0"></iframe>',
            height=500,
        )

# 提示信息
st.info("提示：将视频链接复制到输入框内，点击播放VIP视频按钮即可播放。")
