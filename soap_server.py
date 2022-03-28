from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import subprocess


class PingService(ServiceBase):
    @rpc(String, _returns=String)
    def ping(self, host):
        return subprocess.check_output(['ping', '-c', '2', host]).decode('utf-8')


application = Application([PingService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://0.0.0.0:8090")
    logging.info("wsdl is at: http://0.0.0.0:8090/?wsdl")

    server = make_server('0.0.0.0', 8090, wsgi_application)
    server.serve_forever()