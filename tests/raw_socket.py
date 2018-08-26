import errno
import socket

from twisted.internet import main, reactor
from scapy.layers.l2 import Ether


class RawSocket(object):

    def __init__(self):
        self.sock = socket.socket(
            socket.AF_PACKET, socket.SOCK_RAW, socket.htons(3))
        self.sock.setblocking(0)

    def fileno(self):
        try:
            return self.sock.fileno()
        except socket.error:
            return -1

    def connectionLost(self, reason):
        self.sock.close()
        reactor.removeReader(self)

        # see if there are any poetry sockets left
        for reader in reactor.getReaders():
            if isinstance(reader, RawSocket):
                return
        try:
            reactor.stop()  # no more poetry
        except Exception:
            pass

    def doRead(self):
        while True:
            try:
                bytesread = self.sock.recv(65565)
                if not bytesread:
                    break
                else:
                    packet = Ether(bytesread)
                    if packet.dst != 'ff:ff:ff:ff:ff:ff':
                        break
                    print(packet.src)
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                return main.CONNECTION_LOST

    def logPrefix(self):
        return 'RawSocket'


if __name__ == '__main__':
    reactor.addReader(RawSocket())
    reactor.run()
