from flask import Flask, abort, request
import json

app = Flask(__name__)


@app.route('/payload', methods=['POST'])
def payload():
    if not request.json:
        abort(400)
    print(request.json)
    return json.dumps(request.json)


if __name__ == '__main__':
    app.run(port=4040, debug=True)





'''
import socket
import sys

# Create a socket (SOCK_STREAM means a TCP socket)
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # Connect to server and send data
    sock.connect(('localhost', 4040))
    #sock.sendall(data + "\n")

    # Receive data from the server and shut down
    print("waiting to receive")
    received = sock.recv(1024)
    print("done receiving")
finally:
    sock.close()
    print("close socket")
print("Received: {}".format(received))
'''

'''
#server
import socketserver

class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        # self.request is the TCP socket connected to the client
        self.data = self.request.recv(1024).strip()
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())

if __name__ == "__main__":
    HOST, PORT = "localhost", 5000

    # Create the server, binding to localhost on port 9999
    server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
'''










'''
import http.server
import socketserver

PORT = 8000

Handler = http.server.SimpleHTTPRequestHandler
print("Hello")
with socketserver.TCPServer(('localhost', PORT), Handler) as httpd:
    print("serving at port", PORT)
    httpd.serve_forever()
'''
