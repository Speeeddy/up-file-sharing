import requests
import sys
import base64

if len(sys.argv) == 4:
	sender = sys.argv[1]
	receiver = sys.argv[2]
	filename = sys.argv[3]
else:
	print("Usage: python3 deleter.py <Sender> <Receiver> <File name>")
	sys.exit(0)

URL = "http://nipunsood.ooo/ft"

DATA = {"name":receiver, "sender":sender, "filename":filename}

req = requests.delete(url = URL, json = DATA)
print(req.text)
