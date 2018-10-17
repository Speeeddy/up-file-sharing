import requests
import sys
import base64

if len(args) == 4:
	sender = sys.args[1]
	receiver = sys.args[2]
	filename = sys.args[3]
else:
	print("Usage: python3 upload.py <Sender> <Receiver> <File name>"
	sys.exit()

URL = "nipunsood.ooo/ft"

f = open(filename, "rb")
filadata = base64.b64encode(f.read())

DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}

req = requests.put(url = URL, data = DATA)
print(req.text)
