
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
		print("Setting up server")
		
		#create and bind socket
		print("Creating new socket...")
		self.serverSock = socket(AF_INET, SOCK_STREAM)
		self.serverSock.bind(('', port))
		print("Server socket bound to port %d" % port)

		self.serverSock.listen(5)	#can handle 5 incoming connections at once
		print("Listening...")
		
		#setup for select statement
		inSocks = [self.serverSock]
		outSocks = []
		
		#fixed buffer size of 1kb - maximum length of an IRC message
		bufferSize = 1024
		
		#command functions
		
		def privMsg(prefix, sender, argList):
			
			recp = argList[0]
			msg = ""
			
			#build string
			for word in argList[1:]:
				msg = msg + word
				
			# hash character indicates channel message
			if recp[0] is '#':
				for recChan in self.channelSet:
					if recChan.name == recp:
						recChan.forwardMsg(('%s %s PRIVMSG %s', sender.prefix, recp, msg))
						return
				
				#no channel with that name - make one and add the user!
				newChannel = channel.channel({sender}, recp)
				self.channelSet.add(newChannel)
				newChannel.forwardMsg(('%s %s PRIVMSG %s', sender.prefix, recp, msg))
				return
			
			#privmsg to a user
			else:
				for recUser in selfuserSet:
					if recUser.nick == recp:
						recUser.conn.sendall(('%(pre)s %(nick)s PRIVMSG %(msg)s' % ({'pre': sender.prefix, 'nick': sender.nick, 'msg': msg})).encode('UTF-8'))
						sender.conn.sendall(('%(pre)s %(nick)s PRIVMSG %(msg)s' % ({'pre': sender.prefix, 'nick': sender.nick, 'msg': msg})).encode('UTF-8'))
						return
				
				#no user with that name - error the sender
				sender.conn.sendall((':PyRC.com %s PRIVMSG Error: That user does not exist.' % sender.nick).encode('UTF-8'))
				return
			
			#shouldn't reach here, but if we do, notify sysadmin
			print("privmsg machine broke, have a nice day")
			return #
		
		def nickMsg(prefix, sender, argList):
			print('registering nick...')
			nick = argList[0]
			sender.nick = nick
			sender.prefix = ':%s!%s@PyRC.com' % (sender.nick, sender.nick)
			return
		
		def userMsg(prefix, sender, argList):
			print('Registering user creds...')
			sender.username = argList[0]
			sender.mode = argList[1]
			#argList[2] is unused by IRC
			sender.realname = argList[3]
			return
		
		def joinMsg(prefix, sender, argList):
			print('Joining user to channel...')
			dest = argList[0]
			#make sure the user is joining a valid channel
			if dest[0] is not '#':
				dest = '#' + dest
				
			for destChan in self.channelSet:
				if destChan.name == dest:
					destChan.addUser(sender)
					destChan.forwardMsg('%s JOIN %s' % (prefix, destChan.name))
					return
			
			#channel doesn't exist, create and join the user
			newChannel = channel.channel({sender}, dest)
			self.channelSet.add(newChannel)
			newChannel.forwardMsg('%s JOIN %s' % (prefix, destChan.name))
			return
		
		def partMsg(sender, dest):
			print('Parting user from channel...')
			#make sure the user is leaving a valid channel
			if dest[0] is not '#':
				dest = '#' + dest
				
			for destChan in self.channelSet:
				if destChan.name == dest:
					destChan.removeUser(sender)
					destChan.forwardMsg('%s PART %s' % (prefix, destChan.name))
					return
			
			#channel doesn't exist, send error
			sender.conn.sendall(('%s PRIVMSG Error: That channel doesn\'t exist.' % sender.nick).encode('UTF-8'))
			return
		
		def quitMsg(prefix, sender, argList):
			print('Disconnecting user...')
			if len(argList) is not 0:
				msg = ""
				for word in argList[1:]:
					msg = msg + word
			else:
				msg = 'User Quit'
				
			for leave in self.channelSet:
				leave.removeUser(sender)
				leave.forwardMsg('%s QUIT %s'  % (prefix, msg))
			return
		
		def default(prefix, sender, argList):
			print('Unknown command.')
			sender.conn.sendall((':PyRC.com %s PRIVMSG Error: I do not recognize that command.' % sender.nick).encode('ASCII'))
			return
		#setup for the command dictionary
		cmdDict = {}
		cmdDict['NICK'] = nickMsg
		cmdDict['USER'] = userMsg
		cmdDict['PRIVMSG'] = privMsg
		cmdDict['JOIN'] = joinMsg
		cmdDict['PART'] = partMsg
		cmdDict['QUIT'] = quitMsg
		
		
		#msgHandler - this code implements the message processing that usually comes with an IRC server
		def msgHandler(sender, msg):
			
			msgSplit = msg.split()
			if msg[0] is ':':
				prefix = msgSplit[0]
				cmd = msgSplit[1]
				argSlice = msgSplit[2:]

			else:
				prefix = sender.prefix
				cmd = msgSplit[0]
				argSlice = msgSplit[1:]

			#use the dictionary to find the command we run
			cmdHandler = cmdDict.get(cmd, default)
			cmdHandler(prefix, sender, argSlice)
			sender.conn.sendall(msg.encode('UTF-8'))
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
				
				self.serverSock.close()
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
					print("Accepted connection from %s" % str(addr))
				
				#non-serverSock connection - incoming message
				else:
					msg = s.recv(bufferSize)
					user = self.getUserFromConn(s)
					
					if msg and user:
						msgText = msg.decode('UTF-8')
						print("Received message: %s" % msgText)
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