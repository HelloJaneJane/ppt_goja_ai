from flask import Flask, render_template, request

from app import app

@app.route('/')
def default():
    return render_template('index.html', testStr = "hello world")

@app.route('/test', methods=['POST', 'GET'])
def test():
    if request.method == 'POST':
        print(request.form.to_dict()['html'])
    return render_template('index2.html')

# @app.route('/post', methods=['POST'])
# def post():
#     data = request.form['data']
#     print(data)
#     return data


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000)
    app.run(debug=True)