"""Script to create mysql database"""
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="app",
  password="password"
)

mycursor = mydb.cursor()

mycursor.execute("CREATE DATABASE manifestapp")
mycursor.commit()
mycursor.close()
