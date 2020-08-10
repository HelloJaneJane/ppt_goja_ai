from flask import Flask, render_template, request

from app import app
from convert import convert

@app.route('/')
def default():
    return render_template('index.html', testStr = "hello world")

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        inputHtmlStr = request.form.to_dict()['html']
        convert(inputHtmlStr)
    return render_template('index2.html')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)