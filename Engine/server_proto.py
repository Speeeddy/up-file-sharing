from mySocketAPI import *
from threading import Thread
from threading import Lock
import os

userAddress = dict()
userAddressLock = Lock()
filesPending = dict()
filesPendingLock = Lock()

class ServiceRequests(Thread): 
    # ReceiverInBackground inherits from Thread class, overrides the run() function
    def __init__(self, connection, IP, port): 
        Thread.__init__(self)
        # Call thread constructor 
        self.connection = connection
        self.clientIP = IP
        self.clientPort = port
        print("[+] New server socket thread started for " + IP + ":" + str(port)) 
 
    def run(self): 
    	connection = self.connection
    	global userAddress
    	type = RecvMessageUTF8(connection)
    	if type == "A":					# Client sends an update, inform him about pending file
    		AcknowledgeReceipt(connection)
    		userName = RecvMessageUTF8(connection)
    		userAddressLock.acquire()
    		userAddress[userName] = (self.clientIP, self.clientPort)		#implemet mechanism to timeout old users
    		userAddressLock.release()
    		#AcknowledgeReceipt(connection)
    		print("User: " + userName + ", IP: " + self.clientIP + ":" + str(self.clientPort))

    		pendingFileData = filesPending.get(userName)
    		if pendingFileData is not None:
    			fileName = filesPending[userName][0]
    			sender = filesPending[userName][1]
    			SendFileHandlerClient(fileName, connection, sender, userName)
    			filesPending.pop(userName)								# use locks	
    			os.remove(fileName)
    		else:
    			AcknowledgeReceipt(connection)

    	elif type == "S":				# Client sent a send request
    		AcknowledgeReceipt(connection)
    		sender = RecvMessageUTF8(connection)
    		AcknowledgeReceipt(connection)
    		receiver = RecvMessageUTF8(connection)
    		if receiver in userAddress.keys():
    			fileName = RecvFile(connection)
    			#receiverIP = userAddress[receiver][0]
    			#receiverPort = userAddress[receiver][1]
    			filesPending[receiver] = (fileName, sender)				# Will need to be modified to store more information
    			
    		else:
    			AcknowledgeReceipt(connection, CustomMessage("noUser"))

    		# Now forward the file. Implement storage if user not online here.
    		

def main():
	os.chdir("/tmp")
	serverSocket = CreateServer(Ports=[20000,30000,40000,50000,60000], Listeners=20)		#Spawn server
	threads = []

	while True:
		clientData = AcceptConnection(serverSocket)
		serviceThread = ServiceRequests(clientData["ClientSocket"], clientData["IP"], clientData["Port"])
		threads.append((serviceThread, clientData["ClientSocket"]))
		serviceThread.start()

	# Threads array will keep on becoming bigger and bigger, make mechanism to reduce dead connections
	for t in threads:
		t[0].join()
		t[1].close()

if __name__ == "__main__": main()