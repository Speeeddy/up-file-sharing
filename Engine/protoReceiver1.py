import socket
import os
from threading import Thread 
import sys
import random

def sendMessageUTF8(msg, connection):
	bytesSent = connection.send(msg.encode("UTF-8"))
	return bytesSent

def recvMessageUTF8(connection):
	msg = connection.recv(4096).decode("utf-8").strip()
	return msg
	        
def sendBinary(data, connection):
	bytesSent = connection.send(data)
	return bytesSent
        
def recvBinary(msgLen, fileName, connection):
	bytesReceived = 0
	fileDownloadName = fileName# + "_recv" + str(random.randint(1000,9999))
	f = open(fileDownloadName, "wb")
	while bytesReceived < msgLen:
		data = connection.recv(4096)
		bytesReceived += len(data)
		f.write(data)

	f.close()
	return True

def sendFile(fileName, connection): 
	with open(fileName, 'rb') as f:
		dataBinary = f.read()

	sendMessageUTF8("go")		#I am the sender
	
	msgReceived = ""
	msgReceived = recvMessageUTF8()
	if msgReceived == "name":
		sendMessageUTF8(fileName)		#I am the sender
	
	msgReceived = ""
	msgReceived = recvMessageUTF8()
	if msgReceived == "length":
		fileSize = len(dataBinary)
		sendMessageUTF8(str(fileSize))		#I am the sender

	msgReceived = ""
	msgReceived = recvMessageUTF8()
	if msgReceived == "data":
		fileSentCounter = 0
		while fileSentCounter < fileSize:
			fileEndCounter = (fileSentCounter + 4096) if (fileSentCounter + 4096) < fileSize else fileSize
			# either choose next 4096 bytes, or the remaining bytes ifn <4096 bytes left in file
			bytesSent = sendBinary(dataBinary[fileSentCounter:fileEndCounter])
			fileSentCounter += bytesSent

	msgReceived = ""
	msgReceived = recvMessageUTF8()
	if msgReceived == "done":
		print("Client received file")
		fileList.pop()					#use locks
	else:
		print("Sending failed")

def recvFile(fileList, connection):
	sendMessageUTF8("go")		#I am the sender

	fileName = recvMessageUTF8()
	sendMessageUTF8("go")		#I am the sender

	fileSize = int(recvMessageUTF8())
	sendMessageUTF8("go")		#I am the sender

	fileList.append(fileName)

	if recvBinary(fileSize, fileName) == True:
		sendMessageUTF8("go")		#I am the sender
		print("File " + fileName + " received")
	else:
		sendMessageUTF8("fail")		#I am the sender
		print("Failed to receive file " + fileName)

class ClientThread(Thread): 
    # ClientThread inherits from Thread class, overrides the run() function
	def __init__(self, ip, port, connection, fileList): 
		Thread.__init__(self)
		# Call thread constructor 
		self.ip = ip 
		self.port = port 
		self.connection = connection
		self.fileList = fileList
		print("[+] New server socket thread started for " + ip + ":" + str(port))
	
	def run(self):
		connection = self.connection

		msgReceived = ""
		msgReceived = recvMessageUTF8()
		if msgReceived == "S":
			print("Sender protocol initiated")
			recvFile(fileList, connection)

		if msgReceived == "R":
			print("Receiver protocol initiated")
			if len(fileList) > 0:
				sendFile(fileList[-1], connection)

		print("Server terminating thread")

#CHANGE MAIN - bind and all
def main():
	#if len(sys.argv) > 1:
	#	fileName = sys.argv[1]

	#with open(fileName, "rb") as f:
	#	data = f.read()

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	IP = '127.0.0.1'
	PORT = 37777
	threads = []
	fileList = []
	try:
		sock.bind((IP, PORT))
	except:
		print("Socket already in use?")
		return

	sock.listen(5)

	#try:
	while True:
	    # Server goes on listening forever, till exception or user termination using ^C  
	    print("Waiting for connections from clients...") 
	    (conn, (ip, port)) = sock.accept()
	    newThread = ClientThread(ip, port, conn, fileList)
	    # New object created with IP, port and socket object of the received connection are sent
	    newThread.start() 
	    threads.append((newThread, conn)) 
	    # Keeps a track of created threads, to keep orphan processes in check
	#except:
	#   print("Some problem occured, exiting...\n")

	#finally:
	# These are executed regardless of exceptions, at the end
	for t in threads: 
	    t[1].close()
	    t[0].join() 
	    # All connections are closed while waiting for individual threads to finish
	sock.close()
	# Close the socket connection


if __name__ == "__main__": main()