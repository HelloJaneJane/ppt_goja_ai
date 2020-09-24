from flask import Flask, render_template, request, url_for, redirect, session

from app import app
from server.convert import convert
from server.gpu_api import *

@app.route('/')
def default():
    return render_template('index.html')

@app.route('/ppt', methods=['POST', 'GET'])
def ppt():
    if request.method == 'POST':
        mdeditorHtmlStr = request.form.to_dict()['html']
        downloadUrl = convert(mdeditorHtmlStr) # 다른쓰레드로 처리?
        print(downloadUrl)
        # return render_template('ppt_download_index.html') # 근데 컨버트 주석처리해도 이거 안되는데 왜죠...
        return downloadUrl
        
    return render_template('ppt_index.html')

# @app.route('/ppt/download')
# def pptdownload():
#     return render_template('ppt_download_index.html')

@app.route('/image1', methods=['POST', 'GET'])
def image1():
    if request.method == 'POST':
        inputName = request.form.to_dict()['fileName']
        downloadUrl = backRmvAPI(inputName)
        print(downloadUrl)
        return downloadUrl

    return render_template('img_backRmv_index.html')
    
@app.route('/image2')
def image2():
    return render_template('img_supResol_index.html')
@app.route('/image3')
def image3():
    return render_template('img_iconify_index.html')

@app.route('/contact')
def contact():
    return render_template('contact_index.html')
@app.route('/devinfo')
def devinfo():
    return render_template('devinfo_index.html')
@app.route('/licinfo')
def licinfo():
    return render_template('licinfo_index.html')


@app.route('/login')
def login():
    return render_template('login_index.html')
@app.route('/register')
def register():
    return render_template('register_index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)