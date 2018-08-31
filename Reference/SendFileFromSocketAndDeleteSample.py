import boto3
import socket
import os
from threading import Thread 

# Python2.7 script

# Multithreaded Python server to conduct fetch or delete operations on the S3 buckets

# Created by Nipun Sood, June 2018
# Modified from http://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/


bucketWithImages_name = 'yyyy'
bucketWithRekognitionJSON_name = 'zzzz'
bucketWithFinalJSON_name = 'wwww'
# Change names here if using different buckets

class ClientThread(Thread): 
	# ClientThread inherits from Thread class, overrides the run() function

    def __init__(self,ip,port,connection): 
        Thread.__init__(self) 
		# Call thread constructor 
        self.ip = ip 
        self.port = port 
        self.connection = connection
        print "[+] New server socket thread started for " + ip + ":" + str(port) 

    def run(self): 
		print('connection from ' + self.ip + ":" + str(self.port))
		connection = self.connection
        
		connection.send("what".encode("ASCII"))
		# Send request to UI to specify what operation to perform
		response = connection.recv(4096).decode("ASCII")
			
		if response.strip() == "count":
			# Gives just the count of objects in the buck4compre bucket, by 
			print("Count requested")
			
			count = sum(1 for obj in bucketWithFinalJSON.objects.all())
			# Gets size without creating a list or using memory (traverses headers only)
			# Could use the len(cnt) also
			connection.send(str(count))
			connection.recv(4096)
			# To know that client is ready to receive

		elif response.strip() == "individual":
			# Sends a single file, as requested by the UI
			print("Individual files requested")
						
			unsortedListOfObjects = list(s3Client.list_objects(Bucket=bucketWithFinalJSON_name)['Contents'])
			listOfKeyNames = [obj['Key'] for obj in sorted(unsortedListOfObjects, key=lambda k: k['LastModified'])]
			# The list of object summaries is sorted according to the LastModified parameter, so that
			# in the UI, the oldest image is displayed first.
			# Only key name is stored in list
			count = len(listOfKeyNames)
			
			connection.send("which")
			# Which index number of file

			index = int(connection.recv(4096).decode("ASCII"))
			# File selection is communicated through index numbers, UI has to have list of images beforehand

			if index<0 or index>=count:
				print("Incorrect index '" + str(index) + "', count is " + str(count))
				connection.close()
				return

			jsonName = listOfKeyNames[index]
			# The name of JSON file is the key from the bucket
			name = jsonName[:-5]
			# Name of the image is the the last five characters removed from jsonName (removing ".json" extension)
			
			connection.send(name.encode('ascii'))
			# Send name of file first
			jsonOrImage = connection.recv(4096).decode('ASCII').strip()
			# Whether the UI wants JSON file, or the image also

			if jsonOrImage != "jsononly":
				# Send image also
				with open (name, 'wb') as f:
					bucketWithImages.download_fileobj(name, f)
					f.close()
					# Save image

				with open (jsonName, 'wb') as g:
					bucketWithFinalJSON.download_fileobj(jsonname, g)
					g.close()
					# Save JSON

				with open (jsonName, 'r') as h:
					jsonStr = h.read()
					# Read JSON into a string

				with open (name, 'rb') as k:
					imageData = k.read()
					# Read image into a byte array

				print(name + " local copy saved")

				connection.send(str(len(jsonStr)).encode('ascii'))
				# Length of text sent first
				
				connection.recv(4096)
				# To know that client is ready to receive

				connection.send(jsonStr.encode('utf-8'))
				# JSON data sent. Decode appropriately using UTF8 in the UI

				connection.recv(4096)
				
				connection.send(str(len(imageData)).encode('ascii'))
				# Length of image sent first
				
				connection.recv(4096)
				
				connection.sendall(imageData)
				# Image sent

				os.remove(name)
				os.remove(jsonName)
				# Removes local copy on server
				
				print(name + " local copy removed")

				responseFromUI = connection.recv(4096).decode("ASCII")
				# Response from UI whether successfully received data or not

				if responseFromUI!="true":
					print("whoa, " + responseFromUI + " received")
					raise Exception("DataTransferException")
					# Break control flow if some problem in transmitting

				print(name + " file and text transmitted")
			
			else:
				# When only the JSON file is requested, control enters here

				with open (jsonName, 'wb') as g:
					bucketWithFinalJSON.download_fileobj(jsonName, g)
					g.close()
					# Save JSON data

				with open (jsonName, 'r') as h:
					jsonStr = h.read()
					# Read JSON data
				print(jsonName + " local copy saved")

				connection.send(str(len(jsonStr)).encode('ascii'))
				# Length of text sent first
				
				print(connection.recv(4096))
				# To know that client is ready to receive

				connection.send(jsonStr.encode('utf-8'))
				# Text sent

				os.remove(jsonName)
				# Removes local copy on server
				print(jsonName + " local copy removed")

				responseFromUI = connection.recv(4096).decode("ASCII")
				# Response from UI whether successfully received data or not
				
				if responseFromUI!="true":
					print("whoa, " + responseFromUI + " received")
					raise Exception("DataTransferException")
					# Break control flow if some problem in transmitting

				print(jsonName + " data transmitted")

		elif response.strip() == "all":
			# Get all objects, not individual file calls separately
			filesProcessedCounter = 0
			unsortedListOfObjects = list(s3Client.list_objects(Bucket=bucketWithFinalJSON_name)['Contents'])
			listOfKeyNames = [obj['Key'] for obj in sorted(unsortedListOfObjects, key=lambda k: k['LastModified'])]
			# The list of object summaries is sorted according to the LastModified parameter, so that
			# in the UI, the oldest image is displayed first.
			# Only key name is stored in list
			
			for obj in listOfKeyNames:
				connection.send("true".encode("ASCII"))
				# Received at the UI end to listen for the next image
				# Control moves forward and sends "end" when all the images have been transmitted
				filesProcessedCounter += 1
				
				name = obj[:-5]
				# Removes the ".json" from the end
				jsonName = obj

				print(name + " found")

				with open (name, 'wb') as f:
					bucketWithImages.download_fileobj(name, f)
					f.close()
					# Save the image file

				with open (jsonName, 'wb') as g:
					bucketWithFinalJSON.download_fileobj(jsonName, g)
					g.close()
					# Save the JSON file

				with open (jsonName, 'r') as h:
					jsonStr = h.read()
					# Read the JSON file into a string

				with open (name, 'rb') as k:
					imageData = k.read()
					# Read the image into a byte array

				print(name + " local copy saved")

				connection.recv(4096)
				
				connection.send(name.encode('ascii'))
				# Send name of file first
				
				print(connection.recv(4096))
				# To know that client is ready to receive

				connection.send(str(len(jsonstr)).encode('ascii'))
				# Length of text sent first
				
				print(connection.recv(4096))
				
				connection.send(jsonstr.encode('utf-8'))
				# Text sent
				
				connection.recv(4096)
				
				connection.send(str(len(im)).encode('ascii'))
				# Length of image sent first
				
				connection.recv(4096)
				
				connection.sendall(im)
				# Image sent

				os.remove(name)
				os.remove(obj.key)
				# Removes local copy on server
				
				print(name + " local copy removed")

				responseFromUI = connection.recv(4096).decode("ASCII")
				# To know that client has ended connection

				if responseFromUI!="true":
					print("whoa, " + responseFromUI + " received")
					raise Exception("DataTransferException")

				#print(name + " : text and image transmitted successfully")
				print(str(filesProcessedCounter) + " files and text transmitted")
			# This loop is repeated for every file in the bucket

		elif response.strip() == "delete":
			# will not do anything if name doesn't match

			print("Delete request received")
			connection.send("filename".encode("ASCII"))
			# Requesting image name of the file to delete from the 3 S3 buckets
			# It is assumed that the json files have "reko.json" or ".json" appended at the end of image name

			fileName = connection.recv(4096).decode("ASCII")
			
			print("Deleting " + fileName)
			responseDelete = s3Client.delete_object(
				Bucket=bucketWithImages_name,
				Key=fileName,
				)
			# Image deleted from bucket 2

			fileName_Reko = fileName + "reko.json"
			responseDelete = s3Client.delete_object(
				Bucket=bucketWithRekognitionJSON_name,
				Key=fileName_Reko,
				)
			# Rekognition JSON deleted from bucket 3

			fileName_Compre = fileName + ".json"
			responseDelete = s3Client.delete_object(
				Bucket=bucketWithFinalJSON_name,
				Key=fileName_Compre,
				)
			# Comprehended and corrected JSON deleted from bucket 4

			connection.send("true".encode("ASCII"))
			# Inform UI of success

			connection.recv(4096)
			# Wait for final closing response

		connection.send("end")
		# Close connection on the client side
		
		connection.close()
		print("terminating connection...")

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP 0.0.0.0 allows connection from everywhere
IP = '0.0.0.0'
# AWS security group needs to allow this inbound port
PORT = 37777

# Connect the socket to the port where the server is listening
server_address = (IP, PORT)
print('connecting to {} port {}'.format(*server_address))

sock.bind(server_address)
# Bind IP and port to the socket

s3ConnectionStatus = False
# Connection status initialised to false  

try:
	s3Client = boto3.client('s3')
	# S3 client for uploading and downloading from the buckets
	s3ConnectionStatus = True
except:
	print("Error in s3 connection")
	s3ConnectionStatus = False
	# Redundant statement, but added for clarity. Signifies failure in connection.
	
# Listen for 20 incoming connections, can be scaled according to capability of server
sock.listen(20)

threads = []
try:
    while s3ConnectionStatus:
        # Server goes on listening forever, till exception or user termination using ^C          
        print "Waiting for connections from clients..." 
        (conn, (ip, port)) = sock.accept() 
        newThread = ClientThread(ip,port,conn)
        # New object created with IP, port and socket object of the received connection are sent
        newThread.start() 
        threads.append((newThread, conn)) 
        # Keeps a track of created threads, to keep orphan processes in check

except:
    print("Some problem occured... Exiting")

finally:
    for t in threads: 
        t[1].close()
        t[0].join() 
        # All connections are closed while waiting for individual threads to finish
    sock.close()
