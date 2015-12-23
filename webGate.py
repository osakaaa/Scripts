#!/usr/bin/python
# Simple Web server to handle SMS messages and handle PoCs
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep
import re

PORT_NUMBER = 8080

SMS_TEXT = "test sms text"

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	#Handler for the GET requests
	def do_GET(self):
		global SMS_TEXT
		sendReply = False
		response = "WTF just happened?"
		try:

			if self.path == "/sms":
				mimetype = 'text/plain'
				response = SMS_TEXT
				sendReply = True

			elif self.path.split("?")[0] == "/serve_sms":
				mimetype = 'text/plain'
				print self.path.split("?")[1].split("&")[2]
				try:
					text = self.path.split("?")[1].split("&")[2].split("=")[1]
					SMS_TEXT = re.search("(\d{6})",text).group(1)
				except Exception:
					SMS_TEXT = "ERROR"
				response = "Ok"
				sendReply = True

			elif self.path.endswith('.html'):
				mimetype = 'text/html'
				f = open(curdir + sep + "content" + sep +self.path) 
				response = f.read()
				f.close()
				sendReply = True

			else:
				mimetype = 'text/html'
				response = "<html><h1>This is a test</h1></html>"
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(response)
			return
		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)		
		self.end_headers()
		# Send the html message
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
