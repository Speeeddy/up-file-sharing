# Not injection-secure

import pymysql

dbPassFile = open("DBPass.txt", "r")
dbPass = dbPassFile.read().strip()
print("Password is '" + dbPass + "'")

def insertFilePending(sender, receiver, filename, filehash):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "INSERT INTO FilePending (SENDER, RECEIVER, FILE_NAME, FILE_HASH) VALUES ('{}','{}','{}','{}');".format(sender, receiver, filename, filehash)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in insert file: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	
	

def queryFilePending(receiver):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT SENDER, FILE_NAME, FILE_HASH, TIME_UPLOADED FROM FilePending WHERE RECEIVER = BINARY '{}';".format(receiver)
		n = cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print("DB error in query file: " + str(e))
		db.close()
		return False
	db.close()	
	return result

		
def deleteFilePending(receiver, sender, filename):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "DELETE FROM FilePending WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}' AND FILE_NAME = BINARY '{}';".format(sender, receiver, filename)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in delete file: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True if n > 0 else False	


def insertUser(username, email, number, password, name):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "INSERT INTO USER VALUES ('{}', '{}', '{}', '{}', '{}');".format(username, email, number, password, name)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in insert user: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	

def queryUser(username):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM USER WHERE USERNAME = BINARY '{}';".format(username)
		n = cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print("DB error in query user: " + str(e))
		db.close()
		return False
	db.close()	
	return n

def verifyUser(username, password):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM USER WHERE USERNAME = BINARY '{}' AND PASSWORD = BINARY '{}';".format(username, password)
		n = cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print("DB error in verify user: " + str(e))
		db.close()
		return False
	db.close()	
	return True if n == 1 else False

def deleteUser(username):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		#pendingFiles = queryFilePending(username)
		#for i in pendingFiles:
		#	deleteFilePending(i[0], username, i[1])
		sql = "DELETE FROM USER WHERE USERNAME = BINARY '{}';".format(username)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in delete user: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True if n == 1 else False	

def insertPairing(sender, receiver):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "INSERT INTO Pairing VALUES ('{}', '{}');".format(sender, receiver)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in insert pairing: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	

def verifyPairing(sender, receiver):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender, receiver)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in verify pairing: " + str(e))
		db.close()
		return False
	db.close()	
	return True if n == 1 else False

def deletePairing(sender, receiver):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "DELETE FROM Pairing WHERE SENDER = BINARY '{}' AND RECEIVER = BINARY '{}';".format(sender, receiver)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in delete pairing: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()	
	return True

def deleteAllPairing(sender):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "DELETE FROM Pairing WHERE SENDER = BINARY '{}';".format(sender)
		n = cursor.execute(sql)
		db.commit()
		sql = "DELETE FROM Pairing WHERE RECEIVER = BINARY '{}';".format(sender)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in delete pairing: " + str(e))
		db.rollback()
		db.close()
		return False
	db.close()
	return True

def printLog():
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM FileLog;"
		n = cursor.execute(sql)
		result = cursor.fetchall()
		#for row in result:
		#	print(row)
	except Exception as e:
		print("DB error in query user: " + str(e))
		db.close()
		return False
	db.close()
	return result if n > 0 else False
	
def mainRunner():
	u1 = "_user1"
	u2 = "_user2"
	fn = "_SQLtest.jpg"
	fh = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
	
	if verifyPairing(u1,u2):
		print("Pairing existed already, deleting...")
		if deletePairing(u1,u2):
			print("Pairing deleted")
		else:
			print("Couldn't delete pairing, please check")

	if deleteUser(u1):
		print("User1 existed already, deleting...")

	if deleteUser(u2):
		print("User2 existed already, deleting...")

	if insertUser(u1, "a", "a", "a", "a"):
		print('User 1 added')
		if insertUser(u2, "b", "b", "b", "b"):
			print('User 2 added')
			if insertPairing(u1, u2):
				print("Pairing created")
				if verifyPairing(u1,u2):
					print('Pairing verified')
					if insertFilePending(u1,u2,fn,fh):
						print("File added to pending table")
						print('Now testing downloading')
						print (queryFilePending(u2))
						if deleteFilePending(u2,u1,fn):
							print("File deleted successfully")
							if deletePairing(u1,u2):
								print("Pairing deleted")
								if deleteUser(u1) and deleteUser(u2):
									print("Users deleted")

	logs = printLog()
	if logs:
		print("\nPrinting logs")
		for row in logs:
			print(row)
	else:
		print("No logs found")

	print('Exiting..')

if __name__ == "__main__":
	mainRunner()
