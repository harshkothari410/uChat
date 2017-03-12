from twisted.internet import reactor, protocol

# a client protocol

class EchoClient(protocol.Protocol):
	"""Once connected, send a message, then print the result."""
	def connectionMade(self):
		
		t = raw_input()
		self.transport.write(t)

	def dataReceived(self, data):
		"As soon as any data is received, write it back."
		print "From Server : ", data
		self.transport.loseConnection()

	def connectionLost(self, reason):
		print "connection lost"

class EchoFactory(protocol.ClientFactory):
	protocol = EchoClient

	def clientConnectionFailed(self, connector, reason):
		print "Connection failed - goodbye!"
		reactor.stop()

	def clientConnectionLost(self, connector, reason):
		print "Connection lost - goodbye!"
		reactor.stop()

def main():
	f = EchoFactory()

	reactor.connectTCP("localhost", 8000, f)
	reactor.run()

if __name__ == '__main__':
	main()