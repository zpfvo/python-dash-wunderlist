from __future__ import print_function

import errno
import logging
import socket

from python_dash_wunderlist.txrawudp_reader import RawSocket
from python_dash_wunderlist.types import RECEIVED_RAW_PACKET
from scapy.layers.l2 import Ether
from twisted.internet import main, reactor


class RawSocket(object):

    def __init__(self, callback=None):
        self.callback = callback
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

        try:
            reactor.stop()
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
                    if self.callback:
                        self.callback(packet.src)
            except socket.error as e:
                if e.args[0] == errno.EWOULDBLOCK:
                    break
                return main.CONNECTION_LOST

    def logPrefix(self):
        return 'RawSocket'


def sniffer_middleware(store):
    """scan for dash button arp and udp packets"""
    dispatch = store['dispatch']

    def packet_callback(packet_src):
        logging.debug(packet_src)
        dispatch({
            'type': RECEIVED_RAW_PACKET,
            'src': packet_src,
            'loglevel': 'DEBUG'
        })

    reactor.addReader(RawSocket(packet_callback))

    def wrapper(next_):
        def middleware_dispatcher(action):
            return next_(action)
        return middleware_dispatcher
    return wrapper
