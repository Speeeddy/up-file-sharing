import requests
import sys
import base64
import json

receiver=""

def setReceiver(r):
	global receiver
	receiver = r
def main():
	if len(sys.argv) == 2:
		setReceiver(sys.argv[1])
	else:
		print("Usage: python3 download.py <Receiver>")
		sys.exit(0)

	runner()  	
def runner():
	global receiver
	URLpending = "http://up-karoon.ga/api/fp/"+receiver

	reqGetPending = requests.get(url = URLpending)

	data = json.loads(reqGetPending.text)
#print(data)
#print(type(data))
	if data!="0":
		print("File found!")
		for i in range(len(data)):
			print(str(i+1) + ". Sender: " + data[i][0] + ", File name: " + data[i][1])
		print("Download which file? Enter index")
		index = int(input().strip())-1

		URLfile = "http://up-karoon.ga/api/fp/" + receiver + "/" + data[index][0] + "/" + data[index][1]
		reqGetFile = requests.get(url = URLfile)
		fileData = base64.b64decode(reqGetFile.text)
		f = open("rec_"+data[index][1], "wb")
		f.write(fileData)
		f.close()
		print(data[index][1] + " successfully downloaded as rec_" + data[index][1])
	else:
		return "File not Found"

'''
f = open(filename, "rb")
filedata = base64.b64encode(f.read())

DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}

req = requests.put(url = URL, data = DATA)
print(req.text)
'''
if __name__ == "__main__":
	main()

