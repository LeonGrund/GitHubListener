import socket
import sys
import os
import signal
import select

serversocket = None
def signal_handler(signal, frame):
	print('Ctrl-c -- exiting')
	if serversocket is not None:
		serversocket.close()
		sys.exit(0)

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print("Usage: host, port")
		sys.exit(0)
	else:
		hostname = sys.argv[1]
		port = int(sys.argv[2])
		print('Starting on %s:%d' % (hostname, port))

	print('registering signal')
	signal.signal(signal.SIGINT, signal_handler)
	print('registering signal -- done')

    # create an INET, STREAMing socket
	serversocket = socket.socket(socket.AF_INET,
                                 socket.SOCK_STREAM)
    # bind the socket to a public host, and a well−known port
	serversocket.bind((hostname, port))

	serversocket.listen(5)
	clients = {}
	errorType = None
	errorNum = None

def encode_response(ready_socket, errorNum, errorType):
	header = 'HTTP/1.1 %d %s \r\nContent-Type: text/html\n' % (errorNum, errorType)
	body = ''
	ready_socket.send((header + body + '\r\n\r\n').encode())
	ready_socket.close()
	del clients[ready_socket]
	print(header + body + '\r\n\r\n')




while True:
		rw = [serversocket]
		rw.extend(clients.keys())
		rw,__,__ = select.select(rw, [], [])

		for ready_socket in rw:
			if ready_socket == serversocket:
				(clientsocket, address) = serversocket.accept()
				clients[clientsocket] = ''
				print("serversocket accept!")

			else:
				partial_request = clients[ready_socket]
				data = ready_socket.recv(16384)

				if len(data) == 0:
					# send response to GitHub
					encode_response(ready_socket, 400, 'Bad Request')
					print('Forcing shutdown')
				else:
					request = data.decode("utf-8")
					print(request)
					# update partial http request
					clients[ready_socket] = partial_request + request
					encode_response(ready_socket, 204, 'No Content')
