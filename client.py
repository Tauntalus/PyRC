import time

#client class
class localClient:
	def __init__(self, sock, sockAddr):
		self.conn = sock				#connection port
		self.addr = sockAddr			#connection address
		
		self.nick = ""
		self.userName = ""
		self.mode = 0
		self.realName = ""
		
		self.prefix = "guest!guest@PyRC.com"				#default IRC prefix for sending stuff