from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import socket
import subprocess
from dns import resolver, exception


class PingService(ServiceBase):
    @rpc(String, _returns=String)
    def ping(self, host):
        try:
            return subprocess.check_output(['ping', '-c', '2', host], stderr=subprocess.STDOUT).decode('utf-8')
        except subprocess.CalledProcessError as e:
            return e.output.decode('utf-8')


class DNSService(ServiceBase):
    @rpc(String, _returns=String)
    def dns(self, host):
        try:
            soa = resolver.resolve(host, 'SOA')
            ns = resolver.resolve(host, 'NS')
            mx = resolver.resolve(host, 'MX')

            return f'SOA:\n{soa.rrset.to_text()}\n\nNS:\n{ns.rrset.to_text()}\n\nMX:\n{mx.rrset.to_text()}'
        except exception.DNSException as e:
            return e.__str__()


class ShowIPService(ServiceBase):
    @rpc(String, _returns=String)
    def showip(self, host):
        try:
            return socket.gethostbyname(host)
        except socket.gaierror as e:
            return e.strerror


application = Application([PingService, DNSService, ShowIPService], 'spyne.examples.hello.soap',
                          in_protocol=Soap11(validator='lxml'),
                          out_protocol=Soap11())

wsgi_application = WsgiApplication(application)


if __name__ == '__main__':
    import logging

    from wsgiref.simple_server import make_server

    logging.basicConfig(level=logging.INFO)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.INFO)

    logging.info("listening to http://0.0.0.0:8090")
    logging.info("wsdl is at: http://0.0.0.0:8090/?wsdl")

    server = make_server('0.0.0.0', 8090, wsgi_application)
    server.serve_forever()
