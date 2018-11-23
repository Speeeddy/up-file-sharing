import sqlPy
import pymysql
import unittest
class CLientTest(unittest.TestCase):
	def test_pos_insert_pending(self):
		sender = "yasif"
		receiver = "nipun"
		filename = "newfile"
		filehash = "newhash"
		filesize = 50
		sqlPy.insertFilePending(sender,receiver,filename,filehash,filesize)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "Select * from FilePending where SENDER= BINARY'{}' AND RECEIVER= BINARY'{}'AND FILE_NAME= BINARY '{}' AND FILE_HASH= BINARY'{}' AND FILESIZE= BINARY '{}';".format(sender, receiver, filename, filehash, filesize)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		db.close()
		self.assertNotEqual(res,0)

	def test_neg_insert_pending(self):
		sender = "yasif"
		receiver = "nipun"
		filename = "newfile"
		filehash = "newhash"
		filesize = 50
		sqlPy.insertFilePending(sender,receiver,filename,filehash,filesize)
		receiver = "wrong receiver"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "Select * from FilePending where SENDER= BINARY'{}' AND RECEIVER= BINARY'{}'AND FILE_NAME= BINARY '{}' AND FILE_HASH= BINARY'{}' AND FILESIZE= BINARY '{}';".format(sender, receiver, filename, filehash, filesize)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		db.close()
		self.assertEqual(res,0)

	

if __name__ == '__main__':
	unittest.main()
