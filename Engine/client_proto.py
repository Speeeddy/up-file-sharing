from mySocketAPI import *
from threading import Thread
import time
import sys
from threading import Lock

'''
class ReceiverInBackground(Thread): 
	# ReceiverInBackground inherits from Thread class, overrides the run() function
	def __init__(self, connection): 
		Thread.__init__(self)
		# Call thread constructor 
		self.connection = connection
		#	print("[+] New server socket thread started for " + ip + ":" + str(port))
 
	def run(self): 
		connection = self.connection
		while True:
			recvData = AcceptConnection(connection)
			recvConn = recvData["ClientSocket"]
			#print('Connection from ' + recvConn["IP"] + ":" + str(recvConn["Port"]))
			msgType = RecvMessageUTF8(recvConn)
			if msgType == "S":		#Server wants to send file
				RecvFileHandlerClient(recvConn)
'''
transactionLock = Lock()

class UpdateServerInBackground(Thread):
	def __init__(self, serverIP, serverPort, userName, timer=5):
		Thread.__init__(self)
		self.serverIP = serverIP
		self.serverPort = serverPort
		self.userName = userName
		#self.listeningIP = listeningIP
		#self.listeningPort = listeningPort
		self.timer = timer

	def run(self):
		global transactionLock
		while True:
			transactionLock.acquire()
			#try:
			serverConn = MakeConnection(self.serverIP, self.serverPort)
			#except:
			#	print("Server offline?")
			#	exit()
			SendClientInfo(self.userName, serverConn)
			serverResponse = RecvMessageUTF8(serverConn)
			if serverResponse == "S":
				RecvFileHandlerClient(serverConn)
			elif serverResponse!="go":
				print("Couldn't connect to server")
			CloseConnection(serverConn)
			transactionLock.release()
			time.sleep(self.timer)					# Do it every (for eg.) 5 seconds


def main():
	if len(sys.argv) > 2:
		serverIP = sys.argv[1]
		serverPort = int(sys.argv[2])
	else:
		print("Usage: python3 client.py SERVER_IP SERVER_PORT")
		return

	print("Hello! Please choose a username.")
	userName = input().strip()

	#receiverServer = CreateServer(Ports=[33333,44444,55555])		#Server that the client will listen on for receiving files and messages
	#listeningIP = receiverServer.getsockname()[0]
	#listeningPort = receiverServer.getsockname()[1]
	#receiverThread = ReceiverInBackground(receiverServer)
	#receiverThread.start()

	onlineUpdater = UpdateServerInBackground(serverIP, serverPort, userName)
	onlineUpdater.start()

	global transactionLock

	while True:
		print("Enter S to send a file, E to exit")
		userTextResponse = input().strip()
		transactionLock.acquire()
		if userTextResponse == 'S' or userTextResponse == 's':
			print("Enter full file name (current folder only)")
			fileName = input().strip()
			print("Enter user name of the recepient")
			recepient = input().strip()
			serverConn = MakeConnection(serverIP, serverPort)
			SendFileHandlerClient(fileName, serverConn, userName, recepient)
			CloseConnection(serverConn)

		elif userTextResponse == "E" or userTextResponse == "e":
			transactionLock.release()
			break
		transactionLock.release()

	#receiverThread.exit()
	onlineUpdater.exit()

	print("Good bye!")
	
if __name__ == "__main__": main()