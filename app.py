from flask import Flask, request, render_template
from suds.client import Client

app = Flask(__name__)
client = Client('http://server:8090/?wsdl', cache=None)


@app.route('/', methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        return render_template('ping_form.html')
    elif request.method == 'POST':
        host = request.form['host']
        return render_template('ping.html', host=host, result=client.service.ping(host).split('\n'))


if __name__ == "__main__":
    app.run(debug=True)