import MySQLdb


db = MySQLdb.connect("localhost","root","root")
cursor = db.cursor()
sql = 'CREATE DATABASE web_affiliate'
cursor.execute(sql)