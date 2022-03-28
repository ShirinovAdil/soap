from spyne import Application, rpc, ServiceBase, String
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
import socket
import subprocess
from dns import resolver
import dns.resolver


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
            NS = dns.resolver.resolve(host, 'NS')
            auth_NS = dns.resolver.resolve(host, 'SOA')
            MX = dns.resolver.resolve(host, 'MX')
            for x in NS:
                yield f'NS records: {x.to_text()}'
            for y in auth_NS:
                yield f'authoritative name server: {y.to_text()}'
            for z in MX:
                yield f'MX records: {z.to_text()}'                                
        except socket.gaierror as e:
            return e.strerror


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

    logging.basicConfig(level=logging.DEBUG)
    logging.getLogger('spyne.protocol.xml').setLevel(logging.DEBUG)

    logging.info("listening to http://0.0.0.0:8090")
    logging.info("wsdl is at: http://0.0.0.0:8090/?wsdl")

    server = make_server('0.0.0.0', 8090, wsgi_application)
    server.serve_forever()