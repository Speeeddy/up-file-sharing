import requests
import sys
import base64
import json

if len(sys.argv) == 2:
	receiver = sys.argv[1]
else:
	print("Usage: python3 upload.py <Receiver>")
	sys.exit(0)

URLpending = "http://nipunsood.ooo/fp/"+receiver

reqGetPending = requests.get(url = URLpending)

data = json.loads(reqGetPending.text)
#print(data)
#print(type(data))
if data:
	print("File found!")
	for i in range(len(data)):
		print(str(i+1) + ". Sender: " + data[i][0] + ", File name: " + data[i][1])
	print("Download which file? Enter index")
	index = int(input().strip())-1

	URLfile = "http://nipunsood.ooo/ft/" + receiver + "/" + data[index][0] + "/" + data[index][1]
	reqGetFile = requests.get(url = URLfile)
	fileData = base64.b64decode(reqGetFile.text)
	f = open("rec_"+data[index][1], "wb")
	f.write(fileData)
	f.close()
	print(data[index][1] + " successfully downloaded as rec_" + data[index][1])

'''
f = open(filename, "rb")
filedata = base64.b64encode(f.read())

DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}

req = requests.put(url = URL, data = DATA)
print(req.text)
'''
