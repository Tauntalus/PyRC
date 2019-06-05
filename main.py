import ircServer

port = 50625	#define port for your server here
instance = ircServer.server()
instance.start(port)