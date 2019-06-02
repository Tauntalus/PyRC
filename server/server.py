import "channel/channel.py"

class server:
	def __init__():
		userList = None		#No users on startup
		
		channelList = None	#assign empty list
		channelList.append(channel(None, general))	#add in channel "main"
	
	def __delete__():
		for user in userList:
			user.conn.close()
			
		
	