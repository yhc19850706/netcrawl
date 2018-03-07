#!flask/bin/python
from flask import Flask, jsonify
import cctvjingji
import finance_caijing
app = Flask(__name__)
success ={
    'code': 200,
    'result': u'OK'
}
@app.route('/yhc/api/crawlcaijingtech', methods=['GET'])
def crawlcaijingtech():
    finance_caijing.crawlcaijingtech()
    return jsonify({'result': success})

@app.route('/yhc/api/crawlcaijingfinance', methods=['GET'])
def crawlcaijingfinance():
    finance_caijing.crawlcaijingfinance()
    return jsonify({'result': success})

@app.route('/yhc/api/crawlcctv', methods=['GET'])
def crawlcctv():
    cctvjingji.crawlcctv2()
    return jsonify({'result': success})

if __name__ == '__main__':
    app.run(debug=True)