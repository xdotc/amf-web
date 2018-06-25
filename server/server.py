from http.server import HTTPServer, BaseHTTPRequestHandler
#from io import BytesIO
#import SimpleHTTPServer 
#import SocketServer
import logging
import logging.handlers
import sqlite3
import string
import json
#import requests
import re
import operator
import sys
import subprocess 
from decimal import Decimal
#import urllib.request
import urllib.parse
#from urllib.parse import urlparse
import subprocess

"""
#sqlite3
"""




"""
#logging
"""


logger=logging.getLogger("AMF")
logger.setLevel(logging.DEBUG)

formatter=logging.Formatter('%(asctime)s - %(filename)s - %(name)s  - %(levelname)s - %(message)s')    

fileHandler=logging.FileHandler('AMF.log')
streamHandler=logging.StreamHandler()

fileHandler.setFormatter(formatter)
streamHandler.setFormatter(formatter)

logger.addHandler(fileHandler)
logger.addHandler(streamHandler)

logger.debug("Server start!")



"""
HTTP connection
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):    

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Hello, world!')    
		print('This is GET request. ')


	def do_POST(self):
		content_length = int(self.headers['Content-Length'])

		data = self.rfile.read(content_length).decode('utf-8')
		print(data)
		print(type(data))
		json_data = json.loads(data)
		print(data)
		post_data=urllib.parse.parse_qs(data)


		self.send_response(200)

		print('This is POST request. ')

		print("latitude :", json_data['latitude'])  
		print("longitude :", json_data['longitude']) 
		# print lat, lon info from app

		subprocess.Popen(['python', '/home/controller/amf/server/drone/launch.py', '/dev/ttyUSB0', str(json_data['latitude']), str(json_data['longitude']), '0'])
		#subprocess.Popen(['python3', '/home/controller/amf/server/drone/launch.py', 'sitl', str(json_data['latitude']), str(json_data['longitude']), '0'])
		# connect with drone by transfering lat,lon info

httpd = HTTPServer(('10.0.0.10', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever() 