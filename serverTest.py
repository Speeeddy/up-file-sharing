import unittest
import requests
import base64

class testMethods(unittest.TestCase):
	def setUp(self):
		#filename= open("hehe.jpg","rb")
		#filename.close()
		x=1
	def tearDown(self):
		x=1		
	
	def test_get(self):
		#negative test
		# name = "yasifx"
		# #obj1=server.FilePending()
		# #self.assertEqual(obj1.get(name),('0',404))

		#positive test
		sender = "sid"
		receiver = "yasifx"
		filename = "t.jpg"

		#Upload
		f = open(filename,"rb")
		URL = "http://nipunsood.ooo/ft"
		filedata = base64.b64encode(f.read())
		f.close()
		DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}	
		req = requests.put(url = URL, json = DATA)
		print(req.text)
		
		#Get Pending
		URL = "http://nipunsood.ooo/fp/yasifx"
		req = requests.get(url = URL)
		print(req.text)

		#Download
		URL = "http://nipunsood.ooo/ft/yasifx/sid/t.jpg"
		req = requests.get(url = URL)
		print(req.text)

######################################################

		# TESTING FOR PAIRING AND REGISTRATION 

		username = "sidshas"
		email = "siddharthshah1696@gmail.com"
		number = "12345"
		password = "hello"
		name = "Siddharth Shah"

		username2 = "npsood"
		email2 = "nipunsood@gmail.com"
		number2 = "54321"
		password2 = "hi"
		name2 = "Nipun Sood"
		
		URL = "http://nipunsood.ooo/um"
		DATA = { "username" : username , "email" : email, "number" : number, "password":password, "name":name }
		DATA2 = { "username" : username2 , "email" : email2, "number" : number2, "password":password2, "name":name2 }

		# Create User 1
		req = requests.put(url = URL, json = DATA)
		print(req.text)

		#create User 2
		req = requests.put(url = URL, json = DATA2)
		print(req.text)

		# Initiate Pairing
		url_pairing = "http://nipunsood.ooo/pm"
		data_pairing = { "sender" : username, "receiver" : username2}
		req = requests.put(url = url_pairing, json = data_pairing)
		print(req.text)

		#Double Pairing
		req = requests.put(url = url_pairing, json = data_pairing)
		print(req.text)
	
		#Verify Pairing
		req = requests.get(url = url_pairing, json = data_pairing)
		print(req.text)	

		#Delete Pairing
		req = requests.delete(url = url_pairing, json = data_pairing)
		print(req.text)		

		#Verify Pairing
		req = requests.get(url = url_pairing, json = data_pairing)
		print(req.text)	

		#delete User 1
		req = requests.delete(url = URL, json = DATA)
		print(req.text)

		#delete User 2
		req = requests.delete(url = URL, json = DATA2)
		print(req.text)
	
	def test_put(self):
		self.assertFalse(1==2)
	
	
if __name__ == '__main__':
	unittest.main()
