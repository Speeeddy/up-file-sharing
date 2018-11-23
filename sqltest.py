import sqlPy
import pymysql
import unittest
class CLientTest(unittest.TestCase):

	def test_pos_insertPending(self):
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

	def test_neg_insertPending(self):
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
		len = cursor.rowcount
		db.close()
		self.assertEqual(len,0)

	def test_pos_queryFilePending(self):
		sender = "yasif"
		receiver = "nipun"
		filename = "newfile"
		filehash = "newhash"
		filesize = 50
		sqlPy.insertFilePending(sender,receiver,filename,filehash,filesize)
		res = sqlPy.queryFilePending(receiver)
		self.assertNotEqual(len(res),0)

	def test_neg_queryFilePending(self):
		receiver = "wrong receiver"
		res = sqlPy.queryFilePending(receiver)
		self.assertEqual(len(res),0)

	def test_pos_deleteFilePending(self):
		sender = "ax"
		receiver = "bx"
		filename = "filexx"
		filehash = "newhash"
		filesize = 50
		sqlPy.insertFilePending(sender,receiver,filename,filehash,filesize)
		sqlPy.deleteFilePending(receiver,sender,filename)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "Select * from FilePending where SENDER= BINARY '{}' AND RECEIVER= BINARY '{}'AND FILE_NAME= BINARY '{}';".format(sender, receiver, filename)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		len = cursor.rowcount
		db.close()
		self.assertEqual(len,0)

	def test_neg_deleteFilePending(self):
		sender = "yasif2"
		receiver = "nipun2"
		filename = "newfile2"
		filehash = "newhash2"
		filesize = 50
		sqlPy.insertFilePending(sender,receiver,filename,filehash,filesize)
		filename1 = "wrong file"
		sqlPy.deleteFilePending(receiver,sender,filename1)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "Select * from FilePending where SENDER= BINARY'{}' AND RECEIVER= BINARY'{}'AND FILE_NAME= BINARY '{}';".format(sender, receiver, filename)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		len = cursor.rowcount
		db.close()
		self.assertNotEqual(len,0)
		#cleanup
		sqlPy.deleteFilePending(sender,receiver,filename)

	def test_pos_insertUser(self):
		username = "a2"
		email = "b2@b2.com"
		number = "1234567898"
		password = "newpass"
		name = "newUser"
		sqlPy.insertUser(username, email, number, password, name)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "Select * from USER where USERNAME= BINARY'{}' AND EMAIL= BINARY'{}'AND PHONENO= BINARY '{}' AND PASSWORD = BINARY '{}' AND NAME = BINARY '{}';".format(username, email, number, password, name)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		len = cursor.rowcount
		self.assertNotEqual(len,0)
		#cleanup
		sql = "DELETE from USER where USERNAME= BINARY'{}' AND EMAIL= BINARY'{}'AND PHONENO= BINARY '{}' AND PASSWORD = BINARY '{}' AND NAME = BINARY '{}';".format(username, email, number, password, name)
		n = cursor.execute(sql)
		db.commit()
		db.close()

	def test_pos_queryUser(self):
		username = "pq"
		email = "pq@pq.com"
		number = "1234567898"
		password = "newpass"
		name = "newUser1"
		sqlPy.insertUser(username, email, number, password, name)
		res= sqlPy.queryUser(username)
		self.assertEqual(res, True)
		#cleanup
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		cursor = db.cursor()
		sql = "DELETE from USER where USERNAME= BINARY'{}' AND EMAIL= BINARY'{}'AND PHONENO= BINARY '{}' AND PASSWORD = BINARY '{}' AND NAME = BINARY '{}';".format(username, email, number, password, name)
		n = cursor.execute(sql)
		db.commit()
		db.close()

	def test_neg_queryUser(self):
		username = "newuser"
		email = "new@new.com"
		number = "1234567898"
		password = "newpass1"
		name = "newUser2"
		res= sqlPy.queryUser(username)
		self.assertEqual(res, False)

	def test_pos_verifyUser(self):
		username = "xyz"
		email = "xyz@xyz.com"
		number = "1234567898"
		password = "newpass"
		name = "xyz"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO USER VALUES ('{}', '{}', '{}', '{}', '{}');".format(username, email, number, password, name)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
		res= sqlPy.verifyUser(username,password)
		self.assertEqual(res, True)
		#cleanup
		sql = "DELETE from USER where USERNAME= BINARY'{}' AND EMAIL= BINARY'{}'AND PHONENO= BINARY '{}' AND PASSWORD = BINARY '{}' AND NAME = BINARY '{}';".format(username, email, number, password, name)
		n = cursor.execute(sql)
		db.commit()
		db.close()

	def test_neg_verifyUser(self):
		username = "nouser"
		password = "newpass"
		res= sqlPy.verifyUser(username,password)
		self.assertEqual(res, False)

	def test_pos_deleteUser(self):
		username = "pqr"
		email = "pqr@xyz.com"
		number = "1234567898"
		password = "newpass"
		name = "pqr"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO USER VALUES ('{}', '{}', '{}', '{}', '{}');".format(username, email, number, password, name)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()
		db.close
		res= sqlPy.deleteUser(username)
		self.assertEqual(res, True)
	
	def test_neg_deleteUser(self):
		username = "nouserx"
		password = "newpassx"
		res= sqlPy.deleteUser(username)
		self.assertEqual(res, False)

	def test_pos_verifyPairing(self):
		sender = "sender1"
		receiver = "receiver1"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender,receiver)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()
		res = sqlPy.verifyPairing(sender,receiver)
		self.assertEqual(res,True)
		#cleanup
		sql = "DELETE from Pairing where SENDER= BINARY'{}' AND RECEIVER= BINARY'{}';".format(sender,receiver)
		n = cursor.execute(sql)
		db.commit()
		db.close()

	def test_neg_verifyPairing(self):
		sender = "no_user_a"
		receiver = "no_user_b"
		res = sqlPy.verifyPairing(sender,receiver)
		self.assertEqual(res, False)	

	def test_pos_deletePairing(self):
		sender = "senderxx"
		receiver = "receivexx"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender,receiver)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()

		res = sqlPy.deletePairing(sender,receiver)
		sql = "SELECT * FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender,receiver)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		length = cursor.rowcount
		db.commit()
		db.close()
		self.assertEqual(length,0)
	
	def test_pos_deleteAllPairing(self):
		sender1 = "senderxxx"
		receiver1 = "receiverxxx"
		sender2 = "receiverxxx"
		receiver2 = "senderxxx"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender1,receiver1)
			n = cursor.execute(sql)
			db.commit()
			sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender2,receiver2)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()
		res = sqlPy.deleteAllPairing(sender1)
		sql = "SELECT * FROM Pairing WHERE SENDER = BINARY '{}' OR RECEIVER = BINARY '{}';".format(sender1,receiver2)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		length = cursor.rowcount
		db.commit()
		db.close()
		self.assertEqual(length,0)
		
	def test_pos_getUserHistory(self):
		sender = "edcvfr"
		receiver = "tgb"
		filename =  "new file"
		action = "UPLOAD"
		filesize = 45
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO FileLog(SENDER,RECEIVER,FILENAME,ACTION,FILESIZE) VALUES ('{}', '{}', '{}', '{}', '{}');".format(sender,receiver,filename,action,filesize)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()
		res= sqlPy.getUserHistory(sender)
		self.assertNotEqual(res, False)
		#cleanup
		sql = "DELETE FROM FileLog WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}' AND FILENAME = BINARY '{}' AND ACTION = BINARY '{}' AND FILESIZE = BINARY '{}';".format(sender,receiver,filename,action,filesize)
		n = cursor.execute(sql)
		db.commit()	
		db.close()
	
	def test_neg_getUserHistory(self):
		username = "nouserxx"
		password = "newpassxx"
		res= sqlPy.getUserHistory(username)
		self.assertEqual(res, False)

	def test_pos_incomingPairRequest(self):
		sender = "newUSERxx"
		receiver = "NEWuserxx"
		res = sqlPy.incomingPairRequest(sender,receiver)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "Select * FROM PairPending WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender,receiver)
			n = cursor.execute(sql)
			result = cursor.fetchall()
			length = cursor.rowcount
		except Exception as e:
			print("DB error in Outgoing Pair Request : " + str(e))
			db.rollback()
			db.close()
		self.assertNotEqual(length,0)
		#CLEANUP
		sql = "DELETE FROM PairPending WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}' ;".format(sender,receiver)
		n = cursor.execute(sql)
		db.commit()	
		db.close()

	def test_pos_getPairsRequest(self):
		sender = "newzzzzz"
		receiver = "NEW1zzzz"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = " INSERT INTO Pairing VALUES ('{}','{}');".format(sender,receiver)
			n = cursor.execute(sql)
			result = cursor.fetchall()
			db.commit()
		except Exception as e:
			print("DB error in Outgoing Pair Request : " + str(e))
			db.rollback()
			db.close()
		res = sqlPy.getPairsRequest(receiver)
		self.assertNotEqual(res,False)
		#CLEANUP
		sql = "DELETE FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}' ;".format(sender,receiver)
		n = cursor.execute(sql)
		db.commit()	
		db.close()

	def test_neg_getPairsRequest(self):
		sender = "xx1"
		receiver = "xx2"
		res = sqlPy.getPairsRequest(receiver)
		self.assertEqual(res, False)

	def test_pos_deletePairRequest(self):
		sender = "sendxx"
		receiver = "receivexx"
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender,receiver)
			n = cursor.execute(sql)
			db.commit()
		except Exception as e:
			print("DB error in insert user: " + str(e))
			db.rollback()
			db.close()

		res = sqlPy.deletePairRequest(sender,receiver)
		sql = "SELECT * FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender,receiver)
		n = cursor.execute(sql)
		res = cursor.fetchall()
		length = cursor.rowcount
		db.commit()
		db.close()
		self.assertEqual(length,0)

	def test_pos_insertPairRequest(self):
		sender = "new1"
		receiver = "NEW1"
		res = sqlPy.insertPairRequest(sender,receiver)
		db = pymysql.connect(host='localhost', user='root', password="Qwerty@123", db='up')
		try:
			cursor = db.cursor()
			sql = "Select * FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender,receiver)
			n = cursor.execute(sql)
			result = cursor.fetchall()
			length = cursor.rowcount
		except Exception as e:
			print("DB error in Outgoing Pair Request : " + str(e))
			db.rollback()
			db.close()
		self.assertNotEqual(length,0)
		#CLEANUP
		sql = "DELETE FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}' ;".format(sender,receiver)
		n = cursor.execute(sql)
		db.commit()	
		db.close()
if __name__ == '__main__':
	unittest.main()
