from flask import Flask, Request
from flask_restful import Api, Resource, reqparse
from flask import jsonify
import base64
import json
import os

app = Flask(__name__)
api = Api(app)

pendingFileTable = {}
#format- {receiver : [(sender, filename)]}
#list of tuples - so that if we have multiple files for single receiver

class FilePending(Resource):
	#@app.route('/fp/<string:name>', methods=['GET'])
	def get(self, name):
		#parser = reqparse.RequestParser()
		#parser.add_argument("name")
		#args = parser.parse_args()
		
		#name = args["name"]
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
		
		#parser = reqparse.RequestParser()
		#parser.add_argument("name")
		#parser.add_argument("sender")
		#parser.add_argument("filename")
		#args = parser.parse_args()
		
		#name = args["name"]
		pendingList = pendingFileTable.get(name)
		
		#if (args["sender"], args["filename"]) in pendingList:
		if (sender, filename) in pendingList:
			#load the file
			with open(filename, "rb") as f:
				dataBinary = f.read()
			#b64data = base64.b64encode(dataBinary).decode()
			
			#not encoding here, as file must have come as b64 encoded, and saved as is
			return jsonify({"file" : dataBinary})
		else:
			return "Not found", 404

	#@app.route('/ft', methods=['POST'])
	def post(self):
		# Authenticate
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("sendto")
		parser.add_argument("filename")
		args = parser.parse_args()
		
		name = args["name"]
		receiver = args["sendto"]
		filename = args["filename"]
		
		jsonData = Request.get_json()
		if jsonData == None:
			return "Bad request", 400
		
		#json data should contain base64 encoded file
		dataBinaryEncoded = json.loads(jsonData)["file"]
		#not decoding b64 in server, do it in clientside
		with open(filename, "wb") as g:
			g.write(dataBinaryEncoded)
			g.close()
		
		if pendingFileTable.get(receiver):
			pendingFileTable[receiver].append((name, filename))
		else:
			pendingFileTable[receiver] = [(name, filename)]
		
		return "File uploaded", 200
		
	#@app.route('/ft', methods=['PUT'])
	def put(self):
		return "Invalid", 404	

	#@app.route('/ft', methods=['DELETE'])
	def delete(self):
		#send an explicit delete request when file received
		# Authenticate
		parser = reqparse.RequestParser()
		parser.add_argument("name")
		parser.add_argument("sender")
		parser.add_argument("filename")
		args = parser.parse_args()
		
		name = args["name"]
		sender = args["sender"]
		filename = args["filename"]
		
		pendingList = pendingFileTable.get(name)
		if (sender, filename) in pendingList:
			os.remove(filename)
			pendingFileTable[name].remove((sender, filename))
			return "File deleted", 200
		else:
			return "File not found", 404
		
@app.route('/')
def index():
	return "Hello world!"

api.add_resource(FileTransfer, "/ft", '/ft/<string:name>/<string:sender>/<string:filename>')
api.add_resource(FilePending, "/fp", "/fp/<string:name>")

if __name__ == "__main__": 
	app.run(debug=True)