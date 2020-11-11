from flask import Flask, request
from flask_cors import CORS

from server.awsModule import *

import os

import sys
#sys.path.append(os.path.dirname(os.path.abspath(os.path.dirmame(__file__))))
#os.path.dirnameerror

from gpuEngine import *
from gpuEngine.U2Net import u2net_test as u2test
from gpuEngine import U2Net
from gpuEngine import image_super_resolution
import numpy as np
import asyncio
from PIL import Image
from ISR.models import RDN
from ISR.models import RRDN

async def async_U2Net(outputName):
    u2test.main(outputName)

app=Flask(__name__)
CORS(app)

@app.route("/hello",methods=['GET'])
def hello():
    return "hihi"

@app.route("/backrmv",methods=['POST'])
def backrmv():
    inputName = request.form.to_dict()['fileName']
    outputName = 'backRmv_'+inputName.split('.')[0] + '.png'

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/backgroundRemoval/'+inputName,outputName)

    # background removal 하기
    #loop = asyncio.get_event_loop()
    loop = asyncio.new_event_loop()
    print('new_event_loop()')
    asyncio.set_event_loop(loop)
    print('set_event_loop()')
    loop.run_until_complete(async_U2Net(outputName))
    print('run_until_complete(u2net)')
    loop.close()  
    print('loop.close()')
    
    print(loop.is_closed())
    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/backgroundRemoval/'+outputName)
    print('s3 upload')
    os.remove(outputName)
    print('remove')
    # 파일 다운로드 s3 링크 받아오기
    url = getUrlFromS3('outputImage/backgroundRemoval/'+outputName)

    # 클라이언트로 링크 전송
    return url

@app.route("/supresol",methods=['POST'])
def supresol():
    inputName = request.form.to_dict()['fileName']
    outputName = 'backRmv_'+inputName.split('.')[0] + '.png'

    # 원래 사진 파일 s3에서 다운로드
    downloadFileFromS3('inputImage/superResolution/'+inputName,outputName)
    """
    # super resolution 하기
    # chanel 4 ->3
    img = outputName
#    lr_img = Image.open(img)
#    TypeError: unsupported operand type(s) for /: 'PngImageFile' and 'float'

    lr_img = Image.open(img).convert("RGB")
#    TypeError: unsupported operand type(s) for /: 'Image' and 'float'

    lr_img_np = np.array(lr_img)
    lr_img_f = lr_img_np.astype(float)
    print(lr_img_f.shape)
    print(lr_img_f[0])

    model = RRDN(weights = 'gans')
    sr_img_gan = model.predict(lr_img_f)
    outputName = sr_img_gan
    """
    # 후처리된 사진 파일 s3에 업로드 (+서버에선 파일 지움)
    uploadFileToS3(outputName, 'outputImage/superResolution/'+outputName)
    #os.remove(outputName)

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
