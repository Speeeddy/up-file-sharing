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
		print("Usage: python3 deleter.py <Sender> <Receiver> <File name>")
		sys.exit(0)
	runner()

def runner():
	global receiver
	global filename
	global sender
	URL = "http://nipunsood.ooo/ft"
	
	DATA = {"name":receiver, "sender":sender, "filename":filename}
	
	req = requests.delete(url = URL, json = DATA)
	return req.text

if __name__ == "__main__":
	main()
