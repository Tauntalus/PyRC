import client

#channel class - represents an IRC channel, which is sort of a glorified user ran by the server
class channel:
	
	#init - creates a new channel with a list of connected users and a name
	def __init__(self, userSet, channelName):
		self.userSet = userSet			#list of connected users
		self.name = channelName	#name of channel
		#TODO: Message of the Day fetching and setting
		return
	
	#forwardMsg - Takes a string and sends it to all users connected to the channel
	def forwardMsg(self, msg):
		for user in self.userSet:
			user.conn.send((msg + '\r\n').encode('UTF-8'))
		return
	
	#addUser - takes a user and adds it to the channel's internal list of users
	def addUser(self, user):
		self.userSet.add(user)
		return
	
	#removeUser - takes a user and removes it from the channel, if they are there.
	def removeUser(self, user):
		self.userSet.discard(user)
		return