from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import base64
import json
import os
import boto3, botocore

S3_BUCKET                 = "up-file-transfer-bucket"
S3_LOCATION               = 'http://up-file-transfer-bucket.s3.amazonaws.com/'

app = Flask(__name__)
api = Api(app)

pendingFileTable = {}
#format- {receiver : [(sender, filename)]}
#list of tuples - so that if we have multiple files for single receiver

def upload_file_to_s3(file, bucket_name):

	s3 = boto3.client('s3')
	try:
		s3.upload_file("UserFiles/"+file, S3_BUCKET, file)

	except Exception as e:
		print("Something bad happened during upload : FN = " + file + "; " + e)
		return e

	return "{}{}".format(S3_LOCATION, file)

def download_file_from_s3(file, bucket_name):

	s3 = boto3.client('s3')
	# Download object at bucket-name with key-name to file-like object
	try:
		s3.download_file(S3_BUCKET, file, "UserFiles/"+"s3_"+file)

	except Exception as e:
		print("Something bad happened during download : FN = " + file + "; " + e)
		return e

	return "File downloaded"

class FilePending(Resource):
	#@app.route('/fp/<string:name>', methods=['GET'])
	def get(self, name):
		
		pendingList = pendingFileTable.get(name)
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

		pendingList = pendingFileTable.get(name)
		download_file_from_s3(filename, S3_BUCKET)
		
		if (sender, filename) in pendingList:
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
		return "File uploaded", 200
		
	#@app.route('/ft', methods=['PUT'])
	def put(self):
		# Authenticate
	
		try:
			args = request.get_json(force=True)
			if args == None:
				raise "JsonError"

			name = args["name"]
			receiver = args["sendto"]
			filename = args["filename"]
			dataEncoded = args["data"]
			#not decoding b64 in server, do it in clientside
			with open("UserFiles/"+filename, "w") as g:
				g.write(dataEncoded)
				g.close()
			output = upload_file_to_s3(filename,S3_BUCKET)
			

			if pendingFileTable.get(receiver):
				pendingFileTable[receiver].append((name, filename))
			else:
				pendingFileTable[receiver] = [(name, filename)]
			
			os.remove("UserFiles/"+filename)
			return ""+output, 200

		except Exception as e:			
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
			
			pendingList = pendingFileTable.get(name)
			
			if pendingList and (sender, filename) in pendingList:
				os.remove("UserFiles/"+filename)
				pendingFileTable[name].remove((sender, filename))
				return "File deleted", 200
			else:
				return "File not found", 404
		except:
			return "File not found", 404
					
@app.route('/')
def index():
	return "Hello world!"

api.add_resource(FileTransfer, "/ft", '/ft/<string:name>/<string:sender>/<string:filename>')
api.add_resource(FilePending, "/fp", "/fp/<string:name>")

if __name__ == "__main__": 
	app.run(debug=True)
