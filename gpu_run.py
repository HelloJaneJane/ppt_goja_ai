from flask import Flask, request
from flask_cors import CORS

from server.awsModule import *

app=Flask(__name__)
CORS(app)

@app.route("/hello",methods=['GET'])
def hello():
    return "hihi"

@app.route("/json",methods=['POST'])
def json():
    fileName = request.form.to_dict()['fileName']
    print("파일이름은"+fileName)
    return "success"

@app.route("/backrmv",methods=['POST'])
def backrmv():
    inputName = request.form.to_dict()['fileName']
    print("파일이름은"+inputName)
    outputName = 'backRmv_'+inputName
    downloadFileFromS3('inputImage/backgroundRemoval/'+inputName,outputName)
    # 후처리
    uploadFileToS3(outputName, 'outputImage/backgroundRemoval/'+outputName)
    url = getUrlFromS3('outputImage/backgroundRemoval'+outputName)
    print("파일다운로드경로는"+url)
    return url



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6789, debug=True)
