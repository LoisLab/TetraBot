import netifaces as ni
from http.server import *
import socket
import socketserver
import threading
from http import HTTPStatus

class DefaultRequestHandler(BaseHTTPRequestHandler):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def do_GET(self):
        self.send_response(HTTPStatus.OK)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        try:
            error_msg = ''
            if len(self.path) > 1:
                request = str(self.path[1:])
                self.listener.listen(request)
        except Exception as e:
            error_msg = '<p>' + str(e) + '</p>'
        response = str((self.listener.rotation, self.listener.orientation))
        self.wfile.write(response.encode('utf-8'))
        return
    
    def get_ip_address(self):
        return ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']

class WebServer:
    
    def __init__(self, port, listener, request_handler=DefaultRequestHandler):
        self.port = port
        self.request_handler = request_handler
        request_handler.listener = listener

    def start(self):
        print("Starting web server.")
        self.thread = threading.Thread(target=self.do_start)
        self.thread.start()
        print("Web server started.")

    def do_start(self):
        with ReusableTCPServer(("", self.port), self.request_handler) as httpd:
            print("Serving at port: " + str(self.port))
            self.httpd = httpd
            httpd.serve_forever()
            print("serve_forever() terminated")

    def stop(self):
        # self.httpd.server_close()
        self.httpd.shutdown()
        print("Web server stopped.")

# Allows server to be stopped and restarted on the same port without getting a "Address already in use" error.
# see: https://stackoverflow.com/questions/6380057/python-binding-socket-address-already-in-use/18858817#18858817
class ReusableTCPServer(socketserver.TCPServer):
    def server_bind(self):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.server_address)
