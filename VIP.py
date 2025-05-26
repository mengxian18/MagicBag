导入简报为ST
导入WebBrowser

＃设置页面标题和布局
英石。set_page_config （ page_title = “ vip视频破解工具”，布局= “中心” ）

＃页面标题
英石。标题（“ VIP视频破解工具” ）
英石。Markdown （“作者：Mengxian” ）
＃输入框
video_url = st。text_input （“请输入网页视频链接：”，占位符= “在此输入视频链接...” ）

＃按钮功能
DEF  OPEN_VIDEO （ video_url ）：
    如果Video_url：
        base_url = “ https://jx.xmflv.cc/?url=”
        full_url = base_url + video_url
        webbrowser。打开（ full_url ）
        英石。成功（“正在打开vip视频，请稍候...” ）
    别的：
        英石。错误（“ 请输入有效的视频链接！” ）

＃按钮操作
如果st。按钮（“播放VIP视频” ）：
    open_video （ video_url ）

＃快捷链接
英石。Markdown （“ ###快捷访问平台” ）
COL1，COL2，COL3 = ST。列（3 ）

与Col1：
    如果st。按钮（“爱奇艺” ）：
        webbrowser。打开（“ https://www.iqiyi.com” ）

与Col2：
    如果st。按钮（“腾讯视频” ）：
        webbrowser。打开（“ https://v.qq.com” ）

与Col3：
    如果st。按钮（“优酷视频” ）：
        webbrowser。打开（“ https://www.youku.com/” ）

＃提示信息
英石。info （ “提示：将视频链接复制到输入框内，点击播放vip视频按钮即可播放。” ）
