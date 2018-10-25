import PyMySQL

dbPassFile = open("DBPass.txt", "r")
dbPass = dbPassFile.read()


def insertFilePending(sender, receiver, filename, filehash):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "INSERT INTO FilePending (SENDER, RECEIVER, FILE_NAME, FILE_HASH) VALUES ('%s', '%s', '%s', '%s');"
		n = cursor.execute(sql, (sender, receiver, filename, filehash))
		db.commit()
	except:
		print("DB error in insert file")
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	
	

def queryFilePending(receiver):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "SELECT SENDER, FILE_NAME, FILE_HASH, TIME_UPLOADED FROM FilePending WHERE RECEIVER = '%s';"
		n = cursor.execute(sql, (receiver))
		result = cursor.fetchall()
	except:
		print("DB error in query file")
		db.close()
		return False
	db.close()	
	return result

		
def deleteFilePending(receiver, sender, filename):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "DELETE FROM FilePending WHERE SENDER = '%s' AND RECEIVER = '%s' AND FILE_NAME = '%s';"
		n = cursor.execute(sql, (receiver, sender, filename))
		db.commit()
	except:
		print("DB error in delete file")
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	


def insertUser(username, email, number, password, name):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "INSERT INTO USER VALUES ('%s', '%s', '%s', '%s', '%s');"
		n = cursor.execute(sql, (username, email, number, password, name))
		db.commit()
	except:
		print("DB error in insert user")
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	

def queryUser(username):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM User WHERE USERNAME = '%s';"
		n = cursor.execute(sql, (username))
		result = cursor.fetchall()
	except:
		print("DB error in query user")
		db.close()
		return False
	db.close()	
	if n == 1 return result else return False

def verifyUser(username, password):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM User WHERE USERNAME = '%s' AND PASSWORD = '%s';"
		n = cursor.execute(sql, (username, password))
		result = cursor.fetchall()
	except:
		print("DB error in verify user")
		db.close()
		return False
	db.close()	
	if n == 1 return True else return False

def insertPairing(sender, receiver):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "INSERT INTO Pairing VALUES ('%s', '%s');"
		n = cursor.execute(sql, (sender, receiver))
		db.commit()
	except:
		print("DB error in insert pairing")
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	

def verifyPairing(sender, receiver):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "SELECT * FROM Pairing WHERE SENDER = '%s' AND RECEIVER = '%s';"
		n = cursor.execute(sql, (sender, receiver))
		db.commit()
	except:
		print("DB error in verify pairing")
		db.close()
		return False
	db.close()	
	if n == 1 return True else return False

def deletePairing(sender, receiver):
	db = PyMySQL.connect("localhost", "root", dbPass, "up")
	try:
		cursor = db.cursor()
		sql = "DELETE FROM Pairing WHERE SENDER = '%s' AND RECEIVER = '%s';"
		n = cursor.execute(sql, (receiver, sender))
		db.commit()
	except:
		print("DB error in delete pairing")
		db.rollback()
		db.close()
		return False
	db.close()	
	return True	

