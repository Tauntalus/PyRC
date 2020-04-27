import time

#client class
class localClient:
	def __init__(self, sock, sockAddr):
		self.conn = sock        #connection port
		self.addr = sockAddr    #connection address
		
		self.nick = ""
		self.userName = ""
		self.mode = 0
		self.realName = ""
		
		self.prefix = ""
		return
	
	def setNick(self, nick):
		self.nick = nick
		return
	
	def setUserInfo(self, uname, mode, rname):
		self.userName = uname
		self.mode = mode
		self.realName = rname
		return
		
	def verify(self):
		if (self.nick is not "") and (self.userName is not ""):
			return True
		return False
	
class localUser(localClient):
	def __init__(self, clientBase):
		self.conn = clientBase.conn
		self.addr = clientBase.addr
		
		self.nick = clientBase.nick
		self.userName = clientBase.userName
		self.mode = clientBase.mode
		self.realName = clientBase.realName
		
		self.prefix = self.nick + '!' + self.userName + '@PyRC.com'
		return
	
	def setNick():
		super().setNick(self, nick)
		self.prefix = self.nick + '!' + self.userName + '@PyRC.com'
		return
	
	def setUserInfo(self, uname, mode, realName):
		super().setUserInfo(uname, mode, realName)
		self.prefix = self.nick + '!' + self.userName + '@PyRC.com'
		return
	
	def verify(self):
		return False    #already verified, no need to run verification code again
