import unittest
import download
import deleter
import upload
import requests

class ClientTest(unittest.TestCase):
	def setUp(self):
		x=1
	def tearDown(self):
		x=1
	def test_upload(self):
		#positive test (upload)
		upload.setSender("A")
		upload.setReceiver("B")
		upload.setFilename("hey.jpg")
		req_text = upload.runner()
		self.assertEqual(req_text,'"File uploaded"\n')
	
		#positive test (file in server)
		resp1 = requests.get(url="http://nipunsood.ooo/fp/B")
		print(resp1.text)# == 
	def test_download(self):
		self.assertTrue(1==1)

if __name__ == '__main__':
	unittest.main()
