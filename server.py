from twisted.internet.protocol import Protocol

class Echo(Protocol):

    def dataReceived(self, data):
        print repr(data)
        self.transport.write(data)

from twisted.internet.protocol import Factory
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.internet import reactor

class MyFactory(Factory):

    def buildProtocol(self, addr):
        return Echo()

endpoint = TCP4ServerEndpoint(reactor, 6560)
endpoint.listen(MyFactory())
reactor.run()
