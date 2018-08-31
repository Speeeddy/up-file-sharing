import socket
import sys
import os
import boto3
from threading import Thread 

# Python2.7 script

# Multithreaded Python server to upload files into S3 buckets using socket connections and AWS SDK (boto3)
# Created by Nipun Sood, June 2018
# Modified from http://www.techbeamers.com/python-tutorial-write-multithreaded-python-server/

# First receives file name
# Second receives file size
# Third receives the file itself

bucketImageUpload = "xxxx"
# Name of the first bucket in Nipun Sood's Learning Account, AWS
# Proper access key needs to be specified in `aws configure` in the machine

class ClientThread(Thread): 
    # ClientThread inherits from Thread class, overrides the run() function
    def __init__(self, ip, port, connection): 
        Thread.__init__(self)
        # Call thread constructor 
        self.ip = ip 
        self.port = port 
        self.connection = connection
        print "[+] New server socket thread started for " + ip + ":" + str(port) 
 
    def run(self): 
        print('Connection from ' + self.ip + ":" + str(self.port))
        connection = self.connection
        
        connection.send("g\n")
        # This signals client to send next part, otherwise client
        # might send data together as stream of bytes and it might
        # get read into a single variable erronously

        filename = connection.recv(4096)
        connection.send("g\n")
        
        print("Filename received " + filename)
        # Statement to keep check of progress

        size = int(connection.recv(4096))
        # Size of the file in bytes
        connection.send("g\n")
        
        im = b''
        
        i = 0
        while i < size:
            data = connection.recv(4096)
            im += data
            i += len(data)
        # Loop to capture data that might not fit in a single stream of 4096 bytes

        name = filename
        # Can be modified if a different filename is required to be used for storage

        with open(name, 'wb') as f:
            f.write(im)
            f.close()
        # Writes received data to a new local file

        print(name + " local file created")
        
        s3Client.upload_file(name, bucketImageUpload, name)
        # Uploads file to first bucket with key as the variable 'name'. Exception if permissions not provided.

        print(name + " uploaded to " + bucketImageUpload)
        connection.send("true\n")
        # Indicates to the UI that upload was successful

        os.remove(name)
        # Removes local copy on server

        print(name + " local copy removed")
        connection.close()

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# IP 0.0.0.0 allows connection from everywhere
IP = '0.0.0.0'

# AWS security group needs to allow this inbound port
PORT = 30000

threads = [] 

# Connect the socket to the port where the server is listening
server_address = (IP, PORT)
print('Connecting to {} port {}'.format(*server_address))

sock.bind(server_address)
# Bind IP and port to the socket

s3ConnectionStatus = False
# Connection status initialised to false  

try:
    s3Client = boto3.client('s3')
    # Client to upload to S3 bucket
    s3ConnectionStatus = True

except:
    print("Error in s3 connection")
    s3ConnectionStatus = False
    # Redundant statement, but added for clarity. Signifies failure in connection.

sock.listen(10)
# Limit can be modified according to the capability of the server

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
    print("Some problem occured, exiting...\n")

finally:
    # These are executed regardless of exceptions, at the end
    for t in threads: 
        t[1].close()
        t[0].join() 
        # All connections are closed while waiting for individual threads to finish
    sock.close()
    # Close the socket connection
