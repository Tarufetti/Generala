import mysql.connector

base = mysql.connector.connect('graladice.sql')
c = base.cursor()