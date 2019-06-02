import "channel/channel.py"

class server:
	def __init__():
		userList = None		#No users on startup
		
		channelSet = None	#assign empty list
		channelSet.add(channel(None, general))	#add in channel "main"
	
	def __delete__(self, instance):
		for user in self.userSet:
			user.conn.close()
		for channel in self.channelSet:
			del channel
			
		#just to be sure we've deallocated everything, clear the userSet and channelSet
		self.userSet.clear()
		self.channelSet.clear()
		del self.value
		return
			
		
	