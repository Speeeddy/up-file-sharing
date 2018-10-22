import unittest
import download
import deleter
import upload
import requests
import hashlib
class ClientTest(unittest.TestCase):
	def setUp(self):
		x=1

	def tearDown(self):
		x=1

	def test_pos_upload(self):
		#positive test (upload)
		upload.setSender("p")
		upload.setReceiver("q")
		upload.setFilename("hi.jpg")
		req_text = upload.runner()
		self.assertEqual(req_text,'"File uploaded"\n')

	def test_neg_upload(self):
		#negative test (upload)
		upload.setSender("A1")
		upload.setReceiver("B1")
		upload.setFilename("hehe.jpg")
		req_text = upload.runner()
		self.assertEqual(req_text,"Invalid")

	def test_pos_store(self):
		#positive test (file stored in server)
		resp1 = requests.get(url="http://nipunsood.ooo/fp/B")
		self.assertNotEqual(resp1.text,'"0"\n')

	def test_neg_store(self):
		#negative test(file not stored in server)
		resp1 = requests.get(url="http://nipunsood.ooo/fp/RandomUser")
		self.assertEqual(resp1.text,'"0"\n')
		
	def test_pos_download(self):
		upload.setSender("r")
		upload.setReceiver("c")
		upload.setFilename("t.jpg")
		req_text = upload.runner()
		f1= open("t.jpg","rb")
		hash1 = hashlib.md5(f1.read()).hexdigest()
		f1.close()
		download.setReceiver("c")
		response = download.runner()
		f2= open("rec_t.jpg","rb")
		hash2 = hashlib.md5(f2.read()).hexdigest()
		f2.close()
		self.assertEqual(hash1,hash2)
		
		deleter.setSender("r")
		deleter.setReceiver("c")
		deleter.setFilename("t.jpg")
		response = deleter.runner()
		self.assertEqual(response,'"File deleted"\n')

	def test_neg_download(self):
		download.setReceiver("A1")
		response = download.runner()
		self.assertEqual(response,"File not Found")
	
#	def test_pos_delete(self):
		

	def test_neg_delete(self):
		deleter.setSender("c")
		deleter.setReceiver("d")
		deleter.setFilename("p.jpg")
		response = deleter.runner()
		self.assertEqual(response,'"File not found"\n')

if __name__ == '__main__':
	unittest.main()
