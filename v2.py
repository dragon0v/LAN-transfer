# -*- coding:utf-8 -*-
from flask import *
import json,os
import time
import webbrowser
import socket


# v2对程序进行了大改，原作者可能是初学者
# 多个文件建议打压缩包上传

FILE_PATH = os.path.join(os.path.expanduser('~'),'Desktop','1')
# FILE_PATH = r'''E:\Temp\IDM\新建文件夹'''
PORT = '45450' # http://127.0.0.1:45450

app = Flask(__name__)
app.config.from_object(__name__)
time.sleep(1)
webbrowser.open("http://127.0.0.1:%s"%PORT)
def walk(top):  
    allfiles = dict()
    for root, dirs, files in os.walk(top,followlinks=True):
        for file in files:  
            allfiles[file] = os.path.join(root, file)
    return allfiles

# 首页
@app.route('/')
def index():
    # 获取本机IPv4地址
    import socket
    local_address=[]
    # hostname = socket.gethostname()
    try: 
        s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) 
        s.connect(('8.8.8.8',80)) 
        ip = s.getsockname()[0] 
    finally: 
        s.close() 
    local_address.append(socket.gethostbyname(ip)+':'+PORT)
    
    filepath = FILE_PATH
    if not os.path.exists(filepath):
        os.makedirs(filepath)
    allfiles = walk(filepath)  
    FileName= list(allfiles.keys())  # 历史问题变量名就不改了
    # 下面是一个分页查找
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
    allfiles = walk(filepath)
    FileName= list(allfiles.keys())  # 历史问题变量名就不改了
    
    # 分页
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
    
@app.route('/files/<filename>', methods=['GET'])
def files(filename):
    try:
        filepath = FILE_PATH
        if not os.path.exists(filepath):
            os.makedirs(filepath)
        allfiles = walk(filepath)
        filepath = allfiles[filename]
        return send_file(filepath)
    except Exception as e:
        print(e)
        return json.dumps({'code': filename}, ensure_ascii=False)

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

