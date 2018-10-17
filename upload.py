import requests
import sys
import base64

if len(sys.argv) == 4:
	sender = sys.argv[1]
	receiver = sys.argv[2]
	filename = sys.argv[3]
else:
	print("Usage: python3 upload.py <Sender> <Receiver> <File name>")
	sys.exit(0)

URL = "http://nipunsood.ooo/ft"

f = open(filename, "rb")
filedata = base64.b64encode(f.read())

DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}

req = requests.put(url = URL, data = DATA)
print(req.text)
