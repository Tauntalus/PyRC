import client

#channel class - represents an IRC channel, which is sort of a glorified user ran by the server
class channel:
	
	#init - creates a new channel with a list of connected users and a name
	def __init__(userList, channelName):
		self.userSet = userList			#list of connected users
		self.channelName = channelName	#name of channel
		#TODO: Message of the Day fetching and setting
		return

	#delete - disconnects all existing users and deletes the channel
	def __delete__(self, instance):
		for user in userSet:
			user.conn.close()
			
		self.userSet.clear()
		print("Channel %s was unbound.", self.channelName)
		del self.value
		return
	
	#forwardMsg - Takes a string and sends it to all users connected to the channel
	def forwardMsg(msg):
		for user in self.userSet:
			user.conn.send(msg.encode('ASCII'))
		return
	
	#addUser - takes a user and adds it to the channel's internal list of users
	def addUser(user):
		self.userSet.add(user)
		return
	
	#removeUser - takes a user and removes it from the channel, if they are there.
	def removeUser(user):
		err = self.userList.remove(user)
		if err:
			print("Error removing user %s:", user.nick)
			print(err)
			return -1
		return 0