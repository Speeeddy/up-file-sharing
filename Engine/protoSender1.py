import socket
import os
from threading import Thread 
import sys

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

def sendFile(dataBinary, fileName, connection): 
	sendMessageUTF8("S", connection)		#I am the sender
	
	msgReceived = ""
	msgReceived = recvMessageUTF8(connection)
	if msgReceived != "go":
		print("Received wrong input1 " + msgReceived)
		return

	sendMessageUTF8(fileName, connection)		#I am the sender
	msgReceived = ""
	msgReceived = recvMessageUTF8(connection)
	if msgReceived != "go":
		print("Received wrong input3 " + msgReceived)
		return

	fileSize = len(dataBinary)

	sendMessageUTF8(str(fileSize), connection)		#I am the sender
	msgReceived = ""
	msgReceived = recvMessageUTF8(connection)
	if msgReceived != "go":
		print("Received wrong input4 " + msgReceived)
		return

	fileSentCounter = 0
	while fileSentCounter < fileSize:
		fileEndCounter = (fileSentCounter + 4096) if (fileSentCounter + 4096) < fileSize else fileSize
		# either choose next 4096 bytes, or the remaining bytes ifn <4096 bytes left in file
		bytesSent = sendBinary(dataBinary[fileSentCounter:fileEndCounter], connection)
		fileSentCounter += bytesSent

	msgReceived = ""
	msgReceived = recvMessageUTF8(connection)
	if msgReceived != "go":
		print("Received wrong input5 " + msgReceived)
		return

	print("File sent!")

def recvFile(connection):
	sendMessageUTF8("R", connection)		#I am the sender

	msgReceived = ""
	msgReceived = recvMessageUTF8(connection)
	if msgReceived != "go":
		print("Received wrong input1 " + msgReceived)
		return

	sendMessageUTF8("name", connection)		#I am the sender

	fileName = recvMessageUTF8(connection)
	
	sendMessageUTF8("length", connection)		#I am the sender

	fileSize = int(recvMessageUTF8(connection))
	
	sendMessageUTF8("data", connection)		#I am the sender

	if recvBinary(fileSize, fileName, connection) == True:
		sendMessageUTF8("done", connection)		#I am the sender
		print("File " + fileName + " received")
	else:
		sendMessageUTF8("fail", connection)		#I am the sender
		print("Failed to receive file " + fileName)

def main():
	if len(sys.argv) > 1:
		if sys.argv[1] == "-s":
			fileName = sys.argv[2]
			mode = "s"
		elif sys.argv[1] == "-r":
			mode = "r"

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	IP = '127.0.0.1'
	PORT = 37777

	sock.connect((IP, PORT))
	
	if mode == "s":
		with open(fileName, "rb") as f:
			data = f.read()

		sendFile(data, fileName, sock)

	elif mode == "r":
		recvFile(connection)

	print("File transaction complete")

if __name__ == "__main__": main()