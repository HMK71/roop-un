import os
import gradio as gr
import subprocess
from urllib.parse import urlparse

# 1. WebDAV 登录功能
def mount_webdav(dav_url, username, password):
    # 创建 WebDAV 挂载路径
    mount_point = '/content/webdav'
    os.makedirs(mount_point, exist_ok=True)
    
    # 确认 dav_url 格式是否正确
    parsed_url = urlparse(dav_url)
    if not parsed_url.scheme or not parsed_url.netloc:
        return "Invalid URL format."

    # 使用 davfs2 挂载 WebDAV 文件夹
    try:
        # 使用 pip 安装 davfs2 来挂载 WebDAV
        os.system(f'mount -t davfs {dav_url} {mount_point}')
        # 输入用户名和密码
        os.system(f'echo {username}:{password} > /etc/davfs2/secrets')
        return "登录成功，文件夹已挂载"
    except Exception as e:
        return f"登录失败: {str(e)}"

# 2. 列出 WebDAV 文件夹中的文件
def list_files_in_directory():
    directory = '/content/webdav'
    files = []
    for root, dirs, files_in_dir in os.walk(directory):
        for file in files_in_dir:
            files.append(os.path.join(root, file))
    return files if files else ["目录为空"]

# 3. WebDAV 登录界面
def webdav_interface(dav_url, username, password):
    login_result = mount_webdav(dav_url, username, password)
    if login_result == "登录成功，文件夹已挂载":
        files = list_files_in_directory()  # 登录成功后列出文件
        return login_result, gr.Dropdown(choices=files, label="选择文件")
    else:
        return login_result, None

# 创建 Gradio 页面
def create_webdav_tab():
    with gr.Blocks() as webdav_tab:
        with gr.Row():
            dav_url = gr.Textbox(label="WebDAV URL", placeholder="https://dav.mypikpak.com")
            username = gr.Textbox(label="用户名")
            password = gr.Textbox(label="密码", type="password")
        login_result, file_dropdown = gr.Interface(fn=webdav_interface, 
                                                  inputs=[dav_url, username, password], 
                                                  outputs=[gr.Textbox(), gr.Dropdown()]).launch(share=True)
        
    return webdav_tab

