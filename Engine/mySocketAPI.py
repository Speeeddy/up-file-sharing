import socket
import random

def CreateServer(**kwargs):
	# provide a list as parameter for primary and secondary ports to bind to, in case port already bound
	# Keyword : Ports - List[] of ports
	# Keyword : Listeners - Number of listeners, default is 5

	if kwargs is None:
		print("Valid arguments not provided")
		return None
	else:
		serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		if "Ports" in kwargs.keys():
			IP = "0.0.0.0"
			for PORT in kwargs["Ports"]:
				try:
					serverSocket.bind((IP, PORT))
					print("Successfully bound to port " + str(PORT))
					break
				except:
					print("Port " + str(PORT) + " already in use")
			else:
				print("No port available")
				return
		if "Listeners" in kwargs.keys():
			listeners = kwargs["Listeners"]
			serverSocket.listen(listeners)
			print("Listening for " + str(listeners) + " connections")
		else:
			serverSocket.listen(5)			#default
			print("Listening for 5 connections")

		return serverSocket

def AcceptConnection(serverSocket):
	# Pass the server socket here, and the function to invoke on accepting the connection
	# Do this only after creating the server
	print("Waiting for connection from client..")
	(clientSocket, (IP, PORT)) = serverSocket.accept()
	return {"ClientSocket": clientSocket, "IP": IP, "Port":PORT}
	# Returns a dictionary object 

def CloseConnection(socket_):
	# Simple!
	socket_.close()
	print("Connection closed")

def MakeConnection(**kwargs):
	# Keyword : IP
	# Keyword : Port

	socket_ = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		IP = kwargs["IP"]
		PORT = kwargs["Port"]
		socket_.connect((IP, PORT))
		print("Connection to " + IP + ":" + str(PORT) + " successfully created")
		return socket_
	except:
		print("Invalid arguments provided, or IP/PORT is incorrect. Usage: MakeConnection(IP=\"....\", PORT=1234)")
	return None

def SendMessageUTF8(msg, connection):
	bytesSent = connection.send(msg.encode("UTF-8"))
	return bytesSent

def RecvMessageUTF8(connection):
	msg = connection.recv(4096).decode("utf-8").strip()
	return msg

def SendBinary(data, connection):
	bytesSent = connection.send(data)
	return bytesSent
	        
def RecvBinary(connection):
	data = connection.recv(4096)
	return data

def VerifyAcknowledgeReceipt(connection):
	msg = RecvMessageUTF8(connection)
	if msg == "go":
		return True
	return False

def AcknowledgeReceipt(connection, **kwargs):
	if "CustomMessage" is kwargs.keys():
		SendMessageUTF8(kwargs["CustomMessage"], connection)
	else:
		SendMessageUTF8("go", connection)

def SendFile(fileName, connection):
	# File should be in the current folder
	with open(fileName, "rb") as f:
		dataBinary = f.read() 

	SendMessageUTF8(fileName, connection)	
	if not VerifyAcknowledgeReceipt(connection):
		print("File not send, error #1")
		return

	fileSize = len(dataBinary)
	SendMessageUTF8(str(fileSize), connection)
	if not VerifyAcknowledgeReceipt(connection):
		print("File not send, error #2")
		return

	fileSentCounter = 0
	while fileSentCounter < fileSize:
		fileEndCounter = (fileSentCounter + 4096) if (fileSentCounter + 4096) < fileSize else fileSize
		# either choose next 4096 bytes, or the remaining bytes if <4096 bytes left in file
		bytesSent = SendBinary(dataBinary[fileSentCounter:fileEndCounter], connection)
		fileSentCounter += bytesSent

	if not VerifyAcknowledgeReceipt(connection):
		print("File not send, error #3")
		return

	print("File sent!")

def RecvFile(connection):
	# Let receiver always be the acting-server, acknowledging the messages

	#To start the receive process
	AcknowledgeReceipt(connection)

	fileName = RecvMessageUTF8(connection)
	AcknowledgeReceipt(connection)
	
	fileSize = int(RecvMessageUTF8(connection))
	AcknowledgeReceipt(connection)
	
	bytesReceived = 0
	fileDownloadName = fileName + "_recv" + str(random.randint(1000,9999))
	f = open(fileDownloadName, "wb")

	while bytesReceived < fileSize:
		data = RecvBinary(connection)
		bytesReceived += len(data)
		f.write(data)

	if bytesReceived == fileSize:
		AcknowledgeReceipt(connection)
		f.close()
		print("File " + fileName + " downloaded successfully")
	else:
		AcknowledgeReceipt(connection, CustomMessage="Fail")
		print("Failed to receive file " + fileName)

