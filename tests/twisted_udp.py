from twisted.internet import reactor
from twisted.internet.protocol import DatagramProtocol


class Echo(DatagramProtocol):

    def datagramReceived(self, data, host, port):
        print("received %r from %s:%d" % (data, host, port))


reactor.listenUDP(67, Echo())
reactor.listenUDP(68, Echo())
reactor.run()
