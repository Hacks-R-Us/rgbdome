from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class DomeHTTPServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Nothing here yet!</h1></body></html>")

    def do_HEAD(self):
        self._set_headers()
	 
    def do_POST(self):
        # Doesn't do anything with posted data
	content_length = int(self.headers['Content-Length'])
	post_data = self.rfile.read(content_length)
	self._set_headers()
        self.wfile.write("<html><body><h1>POST recieved</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=DomeHTTPServer, port=80):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print 'Starting httpd...'
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
