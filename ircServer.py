from socket	import *					#socket library
import select							#select helps check for readable/writable channels
import signal							#signal 
import channel							#need the channel definition
import client							#need the client definition


class server:
	
	#init - creates a new server with no users and one channel, general
	def __init__():
		userSet = set()		#No users on startup
		
		channelSet = set()		#assign empty set
		channelSet.add(channel.channel(None, '#general'))	#add in channel "#general"
		return
	
	#delete - disconnect all users, close channels, and delete yourself
	def __delete__(self, instance):
		def handler(sig, frame):
			print("Server shutting down...")
			for user in userSet:
				user.conn.close()
				del user
			for channel in channelSet:
				del channel

			#just to be sure we've deallocated everything, clear the userSet and channelSet
			userSet.clear()
			channelSet.clear()
			del self.value
			print("Sucessful shutdown.")
			exit()
		return handler
	
	def getUserFromConn(conn):
		for user in userSet:
			
		return None
	
	#startServer - gets the server up and ready to run, but not yet in the main while loop
	def start(port):
		print("Setting up server")
		
		#create and bind socket
		print("Creating new socket...")
		serverSock = socket(AF_INET, SOCK_STREAM)
		serverSock.bind(('', port))
		print("Server socket bound to port %d", port)

		serverSock.listen(5)	#can handle 5 incoming connections at once
		print("Listening...")
		
		#setup for select statement
		inSocks = [serverSock]
		outSocks = []
		
		#fixed buffer size of 1kb - maximum length of an IRC message
		bufferSize = 1024
		
		#command functions
		
		def privmsg(sender, recp, msg):
			return
		
		#setup for the command dictionary
		cmdDict = {}
		
		#msgHandler - this code implements the message processing that usually comes with an IRC server
		def msgHandler(msg, user):
			return
		
		#message handling
		while True:
			signal.signal(signal.SIGINT, del)	#If instructed to shut down, delete yourself
			read, write, err = select.select(inSocks, outSocks, inSocks)						#read = readable sockets, write = writable sockets, err = bad sockets
			
			#check each readable socket first
			for s in read:
				
				#serverSock connection = new user
				if s is serverSock:
					
					#accept and setup connection
					conn, addr = s.accept()
					conn.setblocking(0)
					conn.append(inSocks)
					conn.append(outSocks)
					userSet.add(user(conn, addr))
					print("Accepted connection from %s", str(address))
				
				#non-serverSock connection - incoming message
				else:
					msg = s.recv(bufferSize)
					user = getUserFromConn(s)
					
					if msg and user:
						msgText = msg.decode('ASCII')
						print("Received message: %s", msgText)
						handleMessage(msgText, user)
					
					#empty message indicated dead line - quit respectfully
					else:
						handleMessage('QUIT SERVER_SIDE_Dead_Line', user)
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
					print("Server socket bound to port %d", port)
					serverSock.listen(5)
					inSocks.append(serverSock)
					print("Listening...")
					
				else:
					handleMessage('QUIT SERVER_SIDE_Socket_Error', user)
					
		return	#unreachable, but included by convention