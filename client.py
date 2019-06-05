import time

#client class
class localClient:
	def __init__(self, conn, addr):
		self.conn = conn				#connection port
		self.addr = addr				#connection address
		
		self.nick = ""
		self.userName = ""
		self.realName = ""