from flask import Flask, request, render_template
from suds.client import Client

app = Flask(__name__)
client = Client('http://localhost:8090/?wsdl', cache=None)


@app.route('/', methods=['GET', 'POST'])
def ping():
    if request.method == 'GET':
        if 'host' in request.args:
            host = request.args['host']
            return render_template('ping.html', host=host, result=client.service.ping(host).split('\n'))
        else:
            return render_template('ping_form.html')
    elif request.method == 'POST':
        host = request.form['host']
        return render_template('ping.html', host=host, result=client.service.ping(host).split('\n'))


@app.route('/showip', methods=['GET', 'POST'])
def showip():
    if request.method == 'GET':
        if 'host' in request.args:
            host = request.args['host']
            return render_template('showip.html', host=host, result=client.service.showip(host).split('\n'))
        else:
            return render_template('showip_form.html')
    elif request.method == 'POST':
        host = request.form['host']
        return render_template('showip.html', host=host, result=client.service.showip(host).split('\n'))


@app.route('/dns', methods=['GET', 'POST'])
def dns():
    if request.method == 'GET':
        if 'host' in request.args:
            host = request.args['host']
            return render_template('dns.html', host=host, result=client.service.dns(host).split('\n'))
        else:
            return render_template('dns_form.html')
    elif request.method == 'POST':
        host = request.form['host']
        return render_template('dns.html', host=host, result=client.service.dns(host).split('\n'))

    

if __name__ == "__main__":
    app.run(debug=True)
