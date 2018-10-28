from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import base64
import json
import os
import boto3, botocore
from sqlPy import *

S3_BUCKET                 = "up-bucket-brogrammers"
S3_LOCATION               = 'https://s3.ap-south-1.amazonaws.com/up-bucket-brogrammers/'
USE_MYSQL_DB = 1

app = Flask(__name__)
api = Api(app)

pendingFileTable = {}
#format- {receiver : [(sender, filename)]}
#list of tuples - so that if we have multiple files for single receiver

def getEntryFromPendingTable(username):
	#print(16)
	global pendingFileTable
	if USE_MYSQL_DB == 0:
		result = pendingFileTable.get(username)
	#	print(17)
		return result
	else:
		DBresult = queryFilePending(username)
		result = list((i[0], i[1]) for i in DBresult)
		return result

def putEntryIntoPendingTable(receiver, sender, filename, filehash="N/A"):
	#print(10)
	global pendingFileTable
	if USE_MYSQL_DB == 0:
	#	print(11)
		if getEntryFromPendingTable(receiver):
	#		print(12)
			pendingFileTable[receiver].append((sender, filename))
	#		print(13)
		else:
	#		print(14)
			pendingFileTable[receiver] = [(sender, filename)]
	#		print(15)
		return True
	else:
		return insertFilePending(sender, receiver, filename, filehash)
		
def removeEntryFromPendingTable(receiver, sender, filename):
	global pendingFileTable
	if USE_MYSQL_DB == 0:
		pendingFileTable[receiver].remove((sender, filename))
		return True
	else:
		return deleteFilePending(receiver, sender, filename)	

def upload_file_to_s3(file, bucket_name):
	# Replace S3_BUCKET with parameter bucket_name
	s3 = boto3.client('s3')
	try:
		s3.upload_file("UserFiles/"+file, S3_BUCKET, file)

	except Exception as e:
		print("Something bad happened during upload : FN = " + file + "; " + str(e))
		return e

	return "{}{}".format(S3_LOCATION, file)

def download_file_from_s3(file, bucket_name):
	# Replace S3_BUCKET with parameter bucket_name

	s3 = boto3.client('s3')
	# Download object at bucket-name with key-name to file-like object
	try:
		s3.download_file(S3_BUCKET, file, "UserFiles/"+"s3_"+file)

	except Exception as e:
		print("Something bad happened during download : FN = " + file + "; " + str(e))
		return e

	return "File downloaded"

def delete_file_from_s3(file, bucket_name):
	# Replace S3_BUCKET with parameter bucket_name
	s3 = boto3.resource('s3')
	try:
		s3.Object(S3_BUCKET, file).delete()

	except Exception as e:
		print("Something bad happened during delete : FN = " + file + "; " + str(e))
		return e

	return "File deleted!"
	

class FilePending(Resource):
	#@app.route('/fp/<string:name>', methods=['GET'])
	def get(self, name):
		
		pendingList = getEntryFromPendingTable(name)
		#implement a check here against impersonation
		if pendingList:
			return jsonify(pendingList)
		else:
			return "0", 404
	#@app.route('/fp', methods=['POST'])
	def post(self):
		return "Invalid", 404

	#@app.route('/fp', methods=['PUT'])
	def put(self):
		return "Invalid", 404	

	#@app.route('/fp', methods=['DELETE'])
	def delete(self):
		return "Invalid", 404
#after this API, all senders and filename info will be with client
		
class FileTransfer(Resource):
	#@app.route('/ft/<string:name>/<string:sender>/<string:filename>', methods=['GET'])
	def get(self, name, sender, filename):
		#request arguments - name, sender and filename
		
		#get the file. name = file name
		#implement check against impersonation

		pendingList = getEntryFromPendingTable(name)
		
		if pendingList and (sender, filename) in pendingList:
			download_file_from_s3(filename, S3_BUCKET)
			with open("UserFiles/"+"s3_"+filename, "r") as f:
				dataB64 = f.read()

			os.remove("UserFiles/"+"s3_"+filename)
			return dataB64, 200
		else:
			return "Not found", 404

	#@app.route('/ft', methods=['POST'])
	def post(self):
		# not in use, use PUT
		# Authenticate
		return "Use PUT", 404
		
	#@app.route('/ft', methods=['PUT'])
	def put(self):
		# Authenticate
	
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"

	#		print(1)
			name = args["name"]
	#		print(2)
			receiver = args["sendto"]
	#		print(3)
			filename = args["filename"]
	#		print(4)
			dataEncoded = args["data"]
	#		print(5)
			#not decoding b64 in server, do it in clientside
			with open("UserFiles/"+filename, "w") as g:
				g.write(dataEncoded)
				g.close()
	#		print(6)
			output = upload_file_to_s3(filename,S3_BUCKET)
	#		print(7)
			
			putEntryIntoPendingTable(receiver, name, filename)
	#		print(8)
						
			os.remove("UserFiles/"+filename)
			return "File uploaded at "+output, 200

		except Exception as e:
			print("HEREEE " + str(e))			
			return e, 404

	#@app.route('/ft', methods=['DELETE'])
	def delete(self):
		#send an explicit delete request when file received
		# Authenticate
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"

			name = args["name"]
			sender = args["sender"]
			filename = args["filename"]
			
			pendingList = getEntryFromPendingTable(name)
			
			if pendingList and (sender, filename) in pendingList:
				#os.remove("UserFiles/"+filename)
				#pendingFileTable[name].remove((sender, filename))
				# Add S3 file removal support here
				delete_file_from_s3(filename, S3_BUCKET)
				removeEntryFromPendingTable(name, sender, filename)				
				return "File deleted", 200
			else:
				return "File not found", 404
		except:
			return "File deletion exception", 404


class UserManager(Resource):

	def get(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			username = args["username"]
			password = args["password"]
			if verifyUser(username,password):
				return "Verified"
			else:
				return "Invalid credentials",404
		except:
			return "User Verification exception", 404

	def post(self):
		return "Invalid - Use PUT", 404

	def put(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			username = args["username"]
			email = args["email"]
			number = args["number"]
			password = args["password"]
			name = args["name"]
			# Checking if username already in use
			result = queryUser(username)
			if result == False :
				insertUser(username, email, number, password, name)
				return "User Created"
			else:
				return "Username already in use",404
		except:
			return "User Creation exception", 404

	def delete(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			username = args["username"]
			if deleteUser(username):
				# When we delete an account, we remove all pairings associated with it
				if deleteAllPairing(username):
					return username + " account and all its associated pairings deleted"
				else:
					return username + " account deleted but its associated pairings not deleted"
			else:
				return username + " account deletion failed",404
		except:
			return "User deletion exception", 404

class PairingManager(Resource):

	def get(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			sender = args["sender"]
			receiver = args["receiver"]
			if verifyPairing(sender,receiver):
				return "Paired"
			else:
				return "Not Paired",404
		except:
			return "Pairing Verification exception", 404

	def post(self, sender, receiver):
		return "Invalid - Use PUT", 404

	def put(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			sender = args["sender"]
			receiver = args["receiver"]
			# Assuming that we don't have to ask receiver for permission when sender
			# sends pairing request

			# Checking if sender and receiver accounts are active(not been deleted)
			if queryUser(sender) == False:
				return "Pairing Error : "+sender+" has been deleted",404
			if queryUser(receiver) == False:
				return "Pairing Error : "+receiver+" has been deleted",404

			#Checking if pairing already exists
			if verifyPairing(sender,receiver):
				return "Pairing already exists"

			# Initiate Pairing
			if insertPairing(sender,receiver) and insertPairing(receiver,sender):
				return "Pairing Completed"
		except:
			return "Pairing creation exception", 404

	def delete(self):
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"
			sender = args["sender"]
			receiver = args["receiver"]
			if deletePairing(sender,receiver) and deletePairing(receiver,sender):
				return "Pairing removed"
			else:
				return "Error in pairing removal",404
		except:
			return "Pairing Removal exception", 404

@app.route('/')
def index():
	return "Hello world! S3 and DB have been integrated !\nRegistration and Pairing Functionality has been added\n\rBrogrammers send their regards."

api.add_resource(FileTransfer, "/ft", '/ft/<string:name>/<string:sender>/<string:filename>')
api.add_resource(FilePending, "/fp", "/fp/<string:name>")
api.add_resource(UserManager, "/um", "/um/<string:username>/<string:email>/<string:number>/<string:password>/<string:name>")
api.add_resource(PairingManager, "/pm", "/pm/<string:sender>/<string:receiver>")
if __name__ == "__main__": 
	app.run(debug=True)
