from flask import Flask, request
from flask_cors import CORS

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

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=6789, debug=True)
