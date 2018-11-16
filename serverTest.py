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
		# sender = "sidshas"
		# # receiver = "yasifx"
		# filename = "giphy.gif"

		# URL = "https://up-karoon.ga/api/um/check"
		# req = requests.post(url = URL, json = { "username" : " ultra ,sidshas , yasifx,akash,kakka" } )
		# print(req.text)

		DATA = { "sender" : "sidshas" , "receiver" : "akash" }
		DATA2 = { "sender" : "ultra" , "receiver" : "akash" }
		URL = "https://up-karoon.ga/api/pm"
		
		req = requests.put(url = URL, json = DATA2)
		print(req.text)

		req = requests.post(url = URL+"/startPairing", json = DATA2 )
		print(req.text)

		req = requests.post(url = URL+"/getPairs", json = DATA )
		print(req.text)

		# #Upload
		# filename = "heheehe.jpg"
		# f = open(filename,"rb")
		# URL = "https://up-karoon.ga/api/ft"
		# filedata = base64.b64encode(f.read())
		# f.close()
		# DATA = {"name":"sidshas", "sendto":"ultra,akash,nipun", "filename":filename, "data":filedata}	
		# req = requests.put(url = URL, json = DATA)
		# print(req.text)
		
		# # #Get Pending
		# URL = "https://up-karoon.ga/api/fp/sidshas"
		# req = requests.get(url = URL)
		# print(req.text)

		

		# # #Download
		# filename = "giphy.gif"
		# URL = "https://up-karoon.ga/api/ft/sidshas/sidshas/"+filename
		# req = requests.delete(url = URL)
		# print(req.text)

		# sender = "sidshas"
		# URL = "https://up-karoon.ga/api/ft"
		# DATA = {"name":sender, "sender":sender, "filename": "giphy.gif"}
		# req = requests.delete(url = URL, json = DATA )
		# print(req.text)

######################################################

		# TESTING FOR PAIRING AND REGISTRATION 

		# username = "sidshas"
		# email = "siddharthshah1696@gmail.com"
		# number = "12345"
		# password = "hello"
		# name = "Siddharth Shah"

		# username2 = "npsood"
		# email2 = "nipunsood@gmail.com"
		# number2 = "54321"
		# password2 = "hi"
		# name2 = "Nipun Sood"
		
		# URL = "https://up-karoon.ga/api/um"
		# DATA = { "username" : username , "email" : email, "number" : number, "password":password, "name":name }
		# DATA2 = { "username" : username2 , "email" : email2, "number" : number2, "password":password2, "name":name2 }
		# # DATA3 = {"username" : "Speeeddy" ,"password" : "123456"}

		# # #User Check
		# req = requests.post(url = URL+"/check", json = DATA)
		# print(req.text)
		# # # Login check
		# req = requests.post(url = URL+"/login", json = DATA)
		# print(req.text)

		# # # Create User 1
		# req = requests.post(url = URL+"/register", json = DATA)
		# print(req.text)

		# #create User 2
		# req = requests.post(url = URL+"/register", json = DATA2)
		# print(req.text)

		# # Initiate Pairing
		# url_pairing = "https://up-karoon.ga/api/pm"
		# data_pairing = { "sender" : username, "receiver" : username2}
		# req = requests.post(url = url_pairing, json = data_pairing)
		# print(req.text)

		# #Double Pairing
		# req = requests.post(url = url_pairing, json = data_pairing)
		# print(req.text)
	
		# #Verify Pairing
		# req = requests.get(url = url_pairing+"/"+username+"/"+username2, json = data_pairing)
		# print(req.text)	

		# #Delete Pairing
		# req = requests.delete(url = url_pairing, json = data_pairing)
		# print(req.text)		

		# #Verify Pairing
		# req = requests.get(url = url_pairing+"/"+username+"/"+username2, json = data_pairing)
		# print(req.text)	

		#delete User 1
		# req = requests.delete(url = URL, json = DATA)
		# print(req.text)

		# #delete User 2
		# req = requests.delete(url = URL, json = DATA2)
		# print(req.text)
	
	def test_put(self):
		self.assertFalse(1==2)
	
	
if __name__ == '__main__':
	unittest.main()
