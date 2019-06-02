import socket   #networking library

#client class

class client:
	def __init__(conn, addr, nick, general):
		self.conn = conn				#connection port
		self.addr = addr				#connection address
		self.nick = nick				#user nickname
		
		self.channelList = None			#assign empty list
		self.channelList.append(general)# connect to general channel