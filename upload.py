import requests
import sys
import base64
sender=""
receiver=""
filename=""
def setSender(s):
	global sender
	sender = s

def setReceiver(r):
	global receiver
	receiver = r

def setFilename(f):
	global filename
	filename = f

def main():
	if len(sys.argv) == 4:
		setSender(sys.argv[1])
		setReceiver(sys.argv[2])
		setFilename(sys.argv[3])
	else:
		print("Usage: python3 upload.py <Sender> <Receiver> <File name>")
		sys.exit(0)
	runner()

def runner():
	global receiver
	global filename
	global sender
	URL = "http://nipunsood.ooo/ft"
	try:
		f = open(filename, "rb")
		filedata = base64.b64encode(f.read())
	except Exception as e:
		print("Error: " + str(e))
		return "Invalid"
	f.close()
	DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}
	req = requests.put(url = URL, json = DATA)
	requestResult = req.text
	print(requestResult)
	return requestResult

if __name__ == "__main__":
	main()

