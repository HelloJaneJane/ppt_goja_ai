from flask import Flask, request
from flask_cors import CORS

from server.awsModule import *

import os

import sys


from gpuEngine import *
from gpuEngine.U2Net import u2net_test as backRemove

#from U2Net import u2net_test as u2test

app=Flask(__name__)
CORS(app)

@app.route("/hello",methods=['GET'])
def hello():
    return "hihi"

@app.route("/backrmv",methods=['POST'])
def backrmv():
    inputName = request.form.to_dict()['fileName']
    outputName = 'backRmv_' + os.path.splitext(inputName)[0] + '.png'

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/backgroundRemoval/'+inputName,outputName)
    
    #outputNmae = 'test3.png'
    # background removal 하기
    backRemove.main(outputName)

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
    outputName = 'backRmv_' + os.path.splitext(inputName)[0] + '.png'

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/superResolution/'+inputName,outputName)

    #이미지 사이즈 크면 제한하는거 필요함
    
    # super resolution 하기
    # chanel 4 ->3
    outputNmae = 'test3.png'
    img = outputName
    lr_img = np.array(img)
    #Image.fromarray(lr_img)
    model = RRDN(weights = 'gans')
    sr_img_gan = model.predict(lr_img)
    outputName = sr_img_gan

    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/superResolution/'+outputName)
    os.remove(outputName)

    # 파일 다운로드 s3 링크 받아오기
    url = getUrlFromS3('outputImage/superResolution/'+outputName)

    # 클라이언트로 링크 전송
    return url

@app.route("/iconify",methods=['POST'])
def iconify():
    #inputName = request.form.to_dict()['fileName']
    #outputName = 'backRmv_' + os.path.splitext(inputName)[0] + '.png'

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
    #backrmv()
