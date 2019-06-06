
from socket	import *					#socket library
import select							#select helps check for readable/writable channels
import signal							#signal 
import channel							#need the channel definition
import client							#need the client definition


class server:
	
	#init - creates a new server with no users and one channel, general
	def __init__(self):
		self.userSet = set()		#No users on startup
		self.serverSock = None
		self.encoding = 'UTF-8'		#UTF-8 is used universally for IRC nowadays
		self.channelSet = set()		#assign empty set
		self.channelSet.add(channel.channel(set(), '#general'))	#add in channel "#general"
		return
	
	def getUserFromConn(self, conn):
		for user in self.userSet:
			if user.conn is conn:
				return user
		return None
	
	#startServer - gets the server up and ready to run, but not yet in the main while loop
	def start(self, port):
		print('Setting up server')
		
		#create and bind socket
		print('Creating new socket...')
		self.serverSock = socket(AF_INET, SOCK_STREAM)
		self.serverSock.bind(('', port))
		print('Server socket bound to port ' + str(port))

		self.serverSock.listen(5)	#can handle 5 incoming connections at once
		print('Listening...')
		
		#setup for select statement
		inSocks = [self.serverSock]
		outSocks = []
		
		#fixed buffer size of 1kb - maximum length of an IRC message
		bufferSize = 1024
		
		#command functions
		
		def nickMsg(prefix, sender, args, msg):
			nick = args[0]
			for users in self.userSet:
				if users.nick == nick:
					sender.conn.sendall((':PyRC.com 433 * ' + nick + ':That nickname is already in use.\r\n').encode(self.encoding))
					return
				
				sender.setNick(nick)
				if sender.verify():
					sender = client.localUser(sender)
					self.conn.sendall((':PyRC.com 001 ' + self.nick + ': Welcome to the Internet Relay Network ' + self.prefix).encode('UTF-8'))
			return
		
		def userMsg(prefix, sender, args, msg):
			sender.setUserInfo(args[0], args[1], args[3])
			
			if sender.verify():
				sender = client.localUser(sender)
				self.conn.sendall((':PyRC.com 001 ' + self.nick + ': Welcome to the Internet Relay Network ' + self.prefix).encode('UTF-8'))
			return
		
		def joinMsg(prefix, sender, args, msg):
			destName = args[0]
			if destName[0] is not '#':
				destName = '#' + destName
			
			#find channel with same name
			for destChan in self.channelSet:
				if destChan.name == destName:
					destChan.addUser(sender)
					destChan.forwardMsg(prefix + ' ' + msg)
					destChan.forwardMsg(prefix + ' PRIVMSG ' + destChan.name + ' :' + sender.nick + ' has joined the channel.\r\n')
					return
			
			#no channel with same name, make a new one
			destChan = channel.channel({sender}, destName)
			destChan.forwardMsg(prefix + ' ' + msg)
			return
		
		def partMsg(prefix, sender, args, msg):
			destName = args[0]
			if destName[0] is not '#':
				destName = '#' + destName
			
			#find channel with same name
			for destChan in self.channelSet:
				if destChan.name == destName:
					destChan.removeUser(sender)
					destChan.forwardMsg(prefix + " " + msg)
					return
			
			#no channel with same name, throw an error
			sender.conn.sendall((':PyRC.com :That channel does not exist.\r\n').encode(self.encoding))
			return	
		
		def privMsg(prefix, sender, args, msg):
			dest = args[0]
			
			#channel message
			if dest[0] is '#':
				for recChan in self.channelSet:
					if recChan.name == dest:
						recChan.addUser(sender)
						recChan.forwardMsg(prefix + ' ' + msg)
				
				#channel doesn't exist, error
				sender.conn.sendall((':PyRC.com :That channel does not exist.\r\n').encode(self.encoding))
				
			#personal message
			for recp in self.userSet:
				if recp.nick == dest:
					recp.conn.sendall(prefix + ' ' + msg)
					return
			
			#no messages, alert user
			sender.conn.sendall((':PyRC.com :That user does not exist.\r\n').encode(self.encoding))
			return 
		
		def quitMsg(prefix, sender, args, msg):
			for chan in self.channelSet:
				chan.removeUser(sender)
				chan.forwardMsg(prefix + ' ' + msg)
			
			self.userSet.discard(sender)
			return
		
		def meMsg(prefix, sender, args, msg):
			return
		
		def default(prefix, sender, args, msg):
			sender.conn.sendall((':PyRC.com :Your command could not be understood.\r\n').encode(self.encoding))
			return
		
		#setup for the command dictionary
		cmdDict = {}
		cmdDict['NICK'] = nickMsg
		cmdDict['USER'] = userMsg
		cmdDict['PRIVMSG'] = privMsg
		cmdDict['JOIN'] = joinMsg
		cmdDict['PART'] = partMsg
		cmdDict['QUIT'] = quitMsg
		
		cmdDict['ME'] = meMsg
		cmdDict['ACTION'] = meMsg
		
		#msgHandler - this code implements the message processing that usually comes with an IRC server
		def msgHandler(sender, msg):
			
			msgSplit = msg.split()
			if msg[0] is ':':
				prefix = msgSplit[0]
				cmd = msgSplit[1].upper()
				args = msgSplit[2:]

			else:
				prefix = sender.prefix
				cmd = msgSplit[0].upper()
				args = msgSplit[1:]

			#use the dictionary to find the command we run
			cmdHandler = cmdDict.get(cmd, default)
			cmdHandler(prefix, sender, args, msg)
			return
		
		#delete - disconnect all users, close channels, and delete yourself
		def killServer():
			def handler(sig, frame):
				print("Server shutting down...")
				for user in self.userSet:
					user.conn.close()
					del user
				for channel in self.channelSet:
					del channel
				
				self.serverSock.shutdown(0)	#signal we're done
				self.serverSock.detach()	#detach object
				self.serverSock.close()		#destroy object
				del self.serverSock
				print("Sucessful shutdown.")
				exit()
			return handler
	
		#message handling
		while True:
			signal.signal(signal.SIGINT, killServer())	#If instructed to shut down, delete yourself
			read, write, err = select.select(inSocks, outSocks, inSocks)						#read = readable sockets, write = writable sockets, err = bad sockets
			
			#check each readable socket first
			for s in read:
				
				#serverSock connection = new user
				if s is self.serverSock:
					
					#accept and setup connection
					conn, addr = s.accept()
					conn.setblocking(0)
					inSocks.append(conn)
					outSocks.append(conn)
					self.userSet.add(client.localClient(conn, addr))
					print('Accepted connection from ' + str(addr))
				
				#non-serverSock connection - incoming message
				else:
					msg = s.recv(bufferSize)
					user = self.getUserFromConn(s)
					
					if msg and user:
						msgText = msg.decode(self.encoding)
						print('Received message: ' + msgText)
						msgHandler(user, msgText)
					
					#empty message/non-user indicated dead line - quit respectfully
					else:
						msgHandler(user, 'QUIT SERVER_SIDE_Dead_Line')
						inSocks.remove(s)
						outSocks.remove(s)
						
			for s in err:
				#reset server socket
				if s is serverSock:
					print("Detected error in serverSock")
					inSocks.remove(serverSock)
					del serverSock
					print("Creating new socket...")
					serverSock = socket(AF_INET, SOCK_STREAM)
					serverSock.bind('', port)
					print("Server socket bound to port %d" % port)
					serverSock.listen(5)
					inSocks.append(serverSock)
					print("Listening...")
					
				else:
					msgHandler(user, 'QUIT SERVER_SIDE_Socket_Error')
					
		return	#unreachable, but included by convention