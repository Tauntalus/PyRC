import time

#client class
class localClient:
	def __init__(conn, addr):
		self.conn = conn				#connection port
		self.addr = addr				#connection address
		
		self.nick = None
		self.realName = None