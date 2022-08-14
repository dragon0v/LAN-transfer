# -*- coding:utf-8 -*-
from flask import *
import json,os
import time
import webbrowser

# TODO 增加一键下载功能 -当前可以压缩后上传
# TODO 增加文件夹下载？ -当前是遍历读取所有文件
# TODO 重要，删除无效链接 -成功一半吧

FILE_PATH = os.path.join(os.path.expanduser('~'),'Desktop','1')
# FILE_PATH = r'''F:\uTorrentDownloads\Sully.2016.1080p.BluRay.DD5.1.x264-TayTO'''
LOOK_UP = {}

app = Flask(__name__)
app.config.from_object(__name__)
time.sleep(1)
webbrowser.open("http://127.0.0.1:45450")
def GetNameByEveryDir(file_dir):  
    # Input   Root Dir and get all img in per Dir.
    # Out     Every img with its filename and its dir and its path  
    FileNameWithPath = [] 
    FileName         = []
    FileDir          = []
    for root, dirs, files in os.walk(file_dir):  
        for file in files:  
            FileNameWithPath.append(os.path.join(root, file))  # 保存图片路径
            FileName.append(file)                              # 保存图片名称
            FileDir.append(root[len(file_dir):])               # 保存图片所在文件夹
    return FileName,FileNameWithPath,FileDir

# 首页
@app.route('/')
def index():
    # 获取所有的本机IPv4地址列表
    import psutil
    import socket
    local_address=[]
    hostname = socket.gethostname()
    local_address.append(socket.gethostbyname(hostname))
    # local_address = []
    # for name, info in psutil.net_if_addrs().items():
    #     for addr in info:
    #         if addr.address=='127.0.0.1' or addr.address.startswith('192.168'):
    #             pass # 肯定不是这些地址
    #         elif addr.address in LOOK_UP.keys():
    #             if LOOK_UP[addr.address]:
    #                 local_address.append("http://"+addr.address+":45450")
    #         ## 只放入IPv4的地址
    #         elif AddressFamily.AF_INET == addr.family:
    #             temp_url = "http://"+addr.address+":45450"
    #             try:
    #                 t = requests.head(temp_url,timeout=0.2) # 如果正常会返回<Response [200]>
    #                 print(t)                
    #             except requests.exceptions.ConnectionError as ce:
    #                 # local_address.append(temp_url+'xx')
    #                 LOOK_UP[addr.address] = False
    #             except requests.exceptions.ReadTimeout as rt:
    #                 LOOK_UP[addr.address] = True
    #                 local_address.append(temp_url)
    #             else: # 正常时执行
    #                 local_address.append(temp_url)
    
    filepath = FILE_PATH
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    FileName,FileNameWithPath,FileDir = GetNameByEveryDir(filepath)
    page=1
    limit=50
    start = (page - 1) * limit
    end = page * limit if len(FileName) > page * limit else len(FileName)                              
    ret = [FileName[i] for i in range(start, end)]
    all_page=int(len(FileName)/limit)+1
    return render_template('upload.html',file_list=ret,all_file=len(FileName),pages=page,all_page=all_page,address=local_address)


@app.route('/next_page/<int:page>/', methods=['GET'])
def next_page(page):
    filepath = FILE_PATH
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    FileName,FileNameWithPath,FileDir = GetNameByEveryDir(filepath)
    limit = 50
    all_page=int(len(FileName)/limit)+1
    pages = int(page)
    if pages<=0:
        pages=1
    elif pages>=all_page:
        pages=int(all_page)
    else:
        pages=int(page)
    start = (pages - 1) * limit
    end = pages * limit if len(FileName) > pages * limit else len(FileName)
    ret = [FileName[i] for i in range(start, end)]

    return render_template('upload.html',file_list=ret,all_file=len(FileName),pages=pages,all_page=all_page)
    
@app.route('/files/<file_name>', methods=['GET'])
def files(file_name):
    try:
        filepath = FILE_PATH
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        filename =file_name
        # print(file_name)
        file = os.path.join(filepath, filename)
        return send_file(file)
    except Exception as e:
        print(e)
        return json.dumps({'code': "502"}, ensure_ascii=False)

@app.route('/upload', methods=['post'])
def upload():
    try:
        filepath = FILE_PATH
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        print(request.files.getlist('file'))
        for f in request.files.getlist('file'):
            if f:
                filename = f.filename
                upload_path = os.path.join(filepath,filename)
                f.save(upload_path)
        return render_template('upload_ok.html')
    except Exception as e:
        print(e)
        return json.dumps({'code': "502"}, ensure_ascii=False)
    
def run_sever():
    app.run(host='0.0.0.0',port=45450,debug=True)
    
if __name__ == '__main__':
    run_sever()
