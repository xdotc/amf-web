from http.server import HTTPServer, BaseHTTPRequestHandler
from io import BytesIO
import SimpleHTTPServer
import SocketServer
import logging
import logging.handlers
import sqlite3

"""
sqlite3
"""


<<<<<<< HEAD

"""
logging
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
HTTPS connection
"""

class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):    

	def do_GET(self):
		self.send_response(200)
		self.end_headers()
		self.wfile.write(b'Hello, world!')    
		print('This is GET request. ')

	def do_POST(self):
		content_length = int(self.headers['Content-Length'])
		body = self.rfile.read(content_length)
		self.send_response(200)
		response = BytesIO()
		print('This is POST request. ')
		#response.write(b'This is POST request. ')
		#response.write(b'Received: ')
		#response.write(body)
		print(body) 
		#self.wfile.write(response.getvalue())

httpd = HTTPServer(('10.0.0.10', 8080), SimpleHTTPRequestHandler)
httpd.serve_forever()
=======
port_list = ports.serial_ports()
print (port_list)
fleet = Fleet(port_list)
fleet_lock = threading.Lock()

#app_dict entry format: {"instanceID" : [droneID, running_bool]}
app_dict = {}
dict_lock = threading.Lock()

def connect_and_run(instanceID):
    """
    Function to connect and run the drone.
    Sets the drone as running at the end.
    Created to be ran on a new thread so POST response isn't blocked.
    """
    droneid = app_dict[instanceID][0]
    fleet.connect(droneid)
    fleet.run(droneid)
    app_dict[instanceID][1] = True

class Handler(BaseHTTPRequestHandler):

    def _set_headers(self):
        self.send_response(200)
        self.end_headers()

    def log_message(self, format, *args):
        """
        Prevents console from being flooded with the accepted GETs.
        """
        return

    def do_GET(self):
        """
        GET request handler.
        """
        self._set_headers()

        # get instanceID from url
        parsed_path = urlparse.urlparse(self.path)#urlparse는 url을 파싱한 결과로 parseresult 인스턴스를 반환 path는 파일이나 애플리케이션 경로를 의미 http://ssola22.tistory.com/13 
        instanceID = urlparse.parse_qs(parsed_path.query)['instanceID'][0]
        #parse_qs()는 쿼리 문자열을 해석하여 python 자료구조로 변환
        #query는 질의 문자열로 &로 구분된 키=값 쌍 형식으로 표시됨

        #check instanceID is associated with a drone
        if instanceID not in app_dict:
            response = {
                "METHOD": "GET",
                "RESPONSE": -1,
                "DESCRIPTION": "instanceID not in dictionary",
                "LATITUDE": 0,
                "LONGITUDE": 0
            }
        #check if the drone is running. If it is still connecting, you can't get its location
        elif not app_dict[instanceID][1]:
            response = {
                "METHOD": "GET",
                "RESPONSE": -3,
                "DESCRIPTION": "connecting to drone",
                "LATITUDE": 0,
                "LONGITUDE": 0
            }
        else:
            droneid = app_dict[instanceID][0]

            #check for mission end
            if not fleet.mission_ended(droneid):
                lat, lon = fleet.get_location(droneid)

                fleet.log_status(droneid)
                response = {
                    "METHOD": "GET",
                    "RESPONSE": 200,
                    "DESCRIPTION": "mision underway, returning location",
                    "LATITUDE": lat,
                    "LONGITUDE": lon
                }
            else:
                response = {
                    "METHOD": "GET",
                    "RESPONSE": -2,
                    "DESCRIPTION": "mission finished",
                    "LATITUDE": 0,
                    "LONGITUDE": 0
                }
                fleet_lock.acquire()
                fleet.disconnect(droneid)
                fleet_lock.release()

                dict_lock.acquire()
                app_dict.pop(instanceID, None)
                dict_lock.release()
                print("#######disconnecting drone#######")

        self.wfile.write(response)
        self.wfile.write('\n')
        return

    def do_POST(self):
        """
        POST request handler.
        """
        self._set_headers()
        print ("@@@@@ start POST")
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))

        data = simplejson.loads(self.data_string)

        print ("{}").format(data)
        lat = data['latitude']
        lon = data['longitude']

        fleet_lock.acquire()
        droneid = fleet.request(lat, lon)
        fleet_lock.release()

        #check if there is a drone available
        if droneid is not -1:
            appID = data['instanceID']

            dict_lock.acquire()
            app_dict[appID] = [droneid, False]
            dict_lock.release()

            response = {
                "METHOD": "POST",
                "RESPONSE": 200,
                "DESCRIPTION": "drone available",
                "ADDRESS": data['address']
            }

            t = threading.Thread(target=connect_and_run, args=(appID,))
            t.start()
        else:
            response = {
                "METHOD": "POST",
                "RESPONSE": -1,
                "DESCRIPTION": "all drones busy",
                "ADDRESS": data['address']
            }


        self.wfile.write(response)
        self.wfile.write('\n')
        print ("@@@@@ end POST")
        return

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

if __name__ == '__main__':
    if sys.argv[1:]:
        port = int(sys.argv[1])
    else:
        port = 8080
    #server created on current IP
    server = ThreadedHTTPServer(('', port), Handler)
    print ('Starting server, use <Ctrl-C> to stop')
    server.serve_forever()
>>>>>>> fc8861852ea7feec58897882b5b40aee80c66258
