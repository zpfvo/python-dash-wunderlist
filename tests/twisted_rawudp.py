import socket

from twisted.internet import protocol, reactor, udp


class Echo(protocol.DatagramProtocol):

    def datagramReceived(self, data, host, port):
        print(data, host, port)


class RawUDPPort(udp.Port):
    """Raw udp port."""

    socketType = socket.SOCK_RAW  # Overide socket type.


reactor.listenWith(RawUDPPort,
                   proto=Echo(), port=9999, reactor=reactor)
reactor.run()
