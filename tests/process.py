from twisted.internet import reactor, protocol, utils


class MyPP(protocol.ProcessProtocol):

    def outReceived(self, data):
        print("outReceived! with %d bytes!" % len(data))
        print(data)
        # self.data = self.data + data

    def errReceived(self, data):
        print("errReceived! with %d bytes!" % len(data))
        print(data)

    def inConnectionLost(self):
        print("inConnectionLost! stdin is closed! (we probably did it)")

    def outConnectionLost(self):
        print("outConnectionLost! The child closed their stdout!")

    def errConnectionLost(self):
        print("errConnectionLost! The child closed their stderr.")

    def processExited(self, reason):
        print("processExited, status %d" % (reason.value.exitCode,))

    def processEnded(self, reason):
        print("processEnded, status %d" % (reason.value.exitCode,))
        print("quitting")
        reactor.stop()


if __name__ == '__main__':
    reactor.spawnProcess(MyPP(), "pipenv", ["pipenv", "run", "/usr/bin/python3", "/home/florian/workspaces/python/python-dash-wunderlist/bin/dash-button-sniff"])
    # reactor.spawnProcess(MyPP(), "pwd", ["pwd"])
    reactor.run()
