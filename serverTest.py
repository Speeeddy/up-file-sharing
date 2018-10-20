import unittest
#import restflastserver as server
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
		name = "yasifx"
		obj1=server.FilePending()
		self.assertEqual(obj1.get(name),('0',404))

		#positive test
		sender = "nipunxx"
		receiver = "yasifx"
		filename = "he.jpg"
		f = open(filename,"rb")
		URL = "http://nipunsood.ooo/ft"
		filedata = base64.b64encode(f.read())
		f.close()
		DATA = {"name":sender, "sendto":receiver, "filename":filename, "data":filedata}	
		req = requests.put(url = URL, data = DATA)
		obj2=server.FilePending()
		self.assertNotEqual(obj2.get(receiver),('0',404))
	
	def test_put(self):
		self.assertFalse(1==2)
	
	
if __name__ == '__main__':
	unittest.main()
