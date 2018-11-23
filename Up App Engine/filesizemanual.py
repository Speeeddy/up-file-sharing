import boto3
from boto3 import client
import pymysql
import botocore

dbPassFile = open("DBPass.txt", "r")
dbPass = dbPassFile.read().strip()

def querySizeInFilePending(filename):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT FILESIZE FROM FilePending WHERE FILE_NAME = BINARY '{}';".format(filename)
		n = cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print("DB error in query file: " + str(e))
		db.close()
		return False
	db.close()	
	return result

def querySizeInFileLog(filename):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "SELECT FILESIZE FROM FileLog WHERE FILENAME = BINARY '{}';".format(filename)
		n = cursor.execute(sql)
		result = cursor.fetchall()
	except Exception as e:
		print("DB error in query file: " + str(e))
		db.close()
		return False
	db.close()	
	return result

def updateSizeInFilePending(filename, filesize):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "UPDATE FilePending SET FILESIZE = '{}' WHERE FILE_NAME = BINARY \"{}\" AND FILESIZE = 'N/A';".format(filesize, filename)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in query file: " + str(e))
		db.close()
		return 0
	db.close()	
	return n

def updateSizeInFileLog(filename, filesize):
	db = pymysql.connect(host='localhost', user='root', password=dbPass, db='up')
	try:
		cursor = db.cursor()
		sql = "UPDATE FileLog SET FILESIZE = '{}' WHERE FILENAME = BINARY \"{}\" AND FILESIZE = 'N/A';".format(filesize, filename)
		n = cursor.execute(sql)
		db.commit()
	except Exception as e:
		print("DB error in query file: " + str(e))
		db.close()
		return 0
	db.close()	
	return n

S3_BUCKET = "up-bucket-brogrammers"
s3 = boto3.resource('s3')
bucket = s3.Bucket(S3_BUCKET)
s3cl = boto3.client('s3')

fileFound = 0
entriesUpdatedPending = 0
entriesUpdatedLog = 0

for key in bucket.objects.all():
	filename = key.key
	filesizeS3 = int(s3cl.head_object(Bucket=S3_BUCKET, Key=filename)['ResponseMetadata']['HTTPHeaders']['content-length'])
	actualFileSize = int(filesizeS3 * 0.75)
	#sizeSQL = querySizeInFilePending(filename)
	#print(filename + " " + str(sizeSQL) + " " + str(actualFileSize))
	fileFound+=1
	entriesUpdatedPending+=updateSizeInFilePending(filename, actualFileSize)
	entriesUpdatedLog+=updateSizeInFileLog(filename, actualFileSize)

print("Files found: " + str(fileFound))
print("Entries updated in FilePending: " + str(entriesUpdatedPending))
print("Entries updated in FileLog: " + str(entriesUpdatedLog))



#bk = 