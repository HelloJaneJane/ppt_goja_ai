from flask import Flask, request
from flask_cors import CORS

from server.awsModule import *

import os

app=Flask(__name__)
CORS(app)

@app.route("/hello",methods=['GET'])
def hello():
    return "hihi"

@app.route("/backrmv",methods=['POST'])
def backrmv():
    inputName = request.form.to_dict()['fileName']
    outputName = 'backRmv_'+inputName

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/backgroundRemoval/'+inputName,outputName)

    # background removal 하기
    ############
    print("test")

    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/backgroundRemoval/'+outputName)
    os.remove(outputName)

    # 파일 다운로드 s3 링크 받아오기
    url = getUrlFromS3('outputImage/backgroundRemoval/'+outputName)

    # 클라이언트로 링크 전송
    return url

@app.route("/supresol",methods=['POST'])
def supresol():
    inputName = request.form.to_dict()['fileName']
    outputName = 'supResol_'+inputName

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/superResolution/'+inputName,outputName)

    # super resolution 하기
    ############

    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/superResolution/'+outputName)
    os.remove(outputName)

    # 파일 다운로드 s3 링크 받아오기
    url = getUrlFromS3('outputImage/superResolution/'+outputName)

    # 클라이언트로 링크 전송
    return url

@app.route("/iconify",methods=['POST'])
def iconify():
    inputName = request.form.to_dict()['fileName']
    outputName = 'iconify_'+inputName

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/iconify/'+inputName,outputName)

    # iconify 하기
    ############

    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/iconify/'+outputName)
    os.remove(outputName)

    # 파일 다운로드 s3 링크 받아오기
    url = getUrlFromS3('outputImage/iconify/'+outputName)

    # 클라이언트로 링크 전송
    return url


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6789, debug=True)
