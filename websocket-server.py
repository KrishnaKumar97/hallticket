
#NOTE: You will have to update the ip address in index.html

import tornado.ioloop
import tornado.web
import tornado.websocket
import tornado.template
import json, base64

# Python code to demonstrate table creation and 
# insertions with SQL
 
# importing module
import sqlite3
 
# connecting to the database 
connection = sqlite3.connect("hallTicket.db")
 
# cursor 
crsr = connection.cursor()
 
# SQL command to create a table in the database
sql_command = "DROP table student;"
 
# execute the statement
crsr.execute(sql_command)

# SQL command to create a table in the database
sql_command = """CREATE TABLE student ( 
Roll_no INTEGER PRIMARY KEY, 
Name VARCHAR(30), 
Semester INTEGER, 
Branch VARCHAR(20),
Subjects VARCHAR(200), 
Dates VARCHAR(1000), 
photo VARCHAR(100));"""
 
# execute the statement
crsr.execute(sql_command)
 
# SQL command to insert the data in the table
sql_command = """INSERT INTO student VALUES (2564, "Rishabh",4, "Information Science Engineering", "Compiler Design,Graphics,Technical English,Java Programming,Data Structures", "10-10-2018, 11-10-2018, 12-10-2018, 13-10-2018, 14-10-2018", "photos/rishab.jpg");"""
crsr.execute(sql_command)
 
# another SQL command to insert the data in the table
sql_command = """INSERT INTO student VALUES (3509, "John",2, "Electronics and Communication Engineering", "Microprocessor,Electricals,Electronics,Digital Communication,Discrete Mathematics", "10-10-2018, 11-10-2018, 12-10-2018, 13-10-2018, 14-10-2018", "photos/John.jpg");"""
crsr.execute(sql_command)

# another SQL command to insert the data in the table
sql_command = """INSERT INTO student VALUES (1156, "Anne",6, "Computer Science Engineering", "Data Communication,Design Analysis of Algorithm,Scripting Languages,Service Oriented Programming,Data Mining", "10-10-2018, 11-10-2018, 12-10-2018, 13-10-2018, 14-10-2018", "photos/Anne.jpg");"""
crsr.execute(sql_command)
 
 # another SQL command to insert the data in the table
sql_command = """INSERT INTO student VALUES (0897, "Rahul",8, "Mechanical Engineering", "Mettalurgy, Machines", "10-10-2018, 11-10-2018, 12-10-2018", "photos/Rahul.jpg");"""
crsr.execute(sql_command)

# another SQL command to insert the data in the table
sql_command = """INSERT INTO student VALUES (0381, "Siddarth",8, "Aerospace Engineering", "Avionics, Principle of Wind Blades", "10-10-2018, 11-10-2018", "photos/Siddarth.jpg");"""
crsr.execute(sql_command)


# To save the changes in the files. Never skip this. 
# If we skip this, nothing will be saved in the database.
connection.commit()

# execute the command to fetch all the data from the table student
crsr.execute("SELECT * FROM student") 
 
# store all the fetched data in thes ans variable
ans= crsr.fetchall() 
 
# loop to print all the data
for i in ans:
    print(i)
 
# close the connection
connection.close()

class MainHandler(tornado.web.RequestHandler):
  def get(self):
    loader = tornado.template.Loader(".")
    self.write(loader.load("index.html").generate())

class WSHandler(tornado.websocket.WebSocketHandler):
  def open(self):
    print 'connection opened...'

  def on_message(self, message):	
	# connecting to the database 	
	connection = sqlite3.connect("hallTicket.db")	 
	# cursor 
	crsr = connection.cursor()
	# execute the command to fetch all the data from the table student
	crsr.execute("SELECT * FROM student where Roll_no="+message+";") 

	# store all the fetched data in thes ans variable
	ans= crsr.fetchall()
	
	imgData = "";
	with open(ans[0][6], "rb") as imageFile:
		imgData = base64.b64encode(imageFile.read())
		
	data = list(ans[0])
	data[6] = imgData
	data = tuple(data)

	self.write_message(json.dumps(data))
	
	# close the connection
	connection.close()
	
	print 'received:', message

  def on_close(self):
    print 'connection closed...'

application = tornado.web.Application([
  (r'/ws', WSHandler),
  (r'/', MainHandler),
  (r"/(.*)", tornado.web.StaticFileHandler, {"path": "./resources"}),
])

if __name__ == "__main__":
  application.listen(9090)
  tornado.ioloop.IOLoop.instance().start()

