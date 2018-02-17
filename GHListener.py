# -*- coding: utf-8 -*-
import socket
import sys
import signal
import select
import json
import yaml
import subprocess

serversocket = None

def signal_handler(signal, frame):
	print('Ctrl-c -- exiting')
	if serversocket is not None:
		serversocket.close()
		sys.exit(1)

if __name__ == "__main__":

	if len(sys.argv) >= 2 and sys.argv[1] != '1':
		print("UNTRUSTED INPUT, EXIT")
		sys.exit(1)

	# run test
	if len(sys.argv) >= 2 and sys.argv[1] == '1':
		run_test_script = subprocess.check_output(['python', 'testGHL.py'], stderr=subprocess.PIPE)
		print(run_test_script.decode())
		print("TEST FINISHED")
		sys.exit(0)
	else:
		hostname = 'localhost'
		port = 4000
		print('Starting on %s:%d' % (hostname, port))

	print('registering signal')
	signal.signal(signal.SIGINT, signal_handler)
	print('registering signal -- done') # create an INET, STREAMing socket
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # bind the socket to a public host, and a well−known port
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
	#print(header + body + '\r\n\r\n')


# retruns event, repo, branch name
def read_POST(ready_socket):

	data = clients[ready_socket]

	header = data.split('\r\n\r\n')[0]
	event = header.split('\r\n')[4]
	eventName = event[16:]

	payload = data.split('\r\n\r\n')[1]
	dic = json.loads(payload)
	repoName = dic['repository']['name']

	branch = dic['ref'][11:]

	print('========================')
	print(eventName)
	print(repoName)
	print(branch)
	print('========================')

	# Override clients dic request data with event, repo, and branch name
	# ['event','repo','branch']
	clients[ready_socket] = {'event':eventName, 'repo':repoName, 'branch':branch}

def read_composefile(ready_socket):

	EVENT = clients[ready_socket]['event']
	REPO = clients[ready_socket]['repo']
	BRANCH = clients[ready_socket]['branch']

	yml_file = '../' + REPO + '/docker-commands.yaml'
	# check for valid event, reop, and branch
	if (EVENT == 'push'):
		with open(yml_file, 'r') as stream:
			composeYML = yaml.safe_load(stream)
			# add clients docker-commands data
			clients[ready_socket]['stage'] = composeYML

def check_yaml(ready_socket):

	stage = clients[ready_socket]['stage']
	EVENT = clients[ready_socket]['event']
	REPO = clients[ready_socket]['repo']
	BRANCH = clients[ready_socket]['branch']

	# check build stage
	print(stage)

	try:
		DOCKER = stage['build'][0] if stage['build'][0] == 'docker' else -1
		BUILD = stage['build'][1] if stage['build'][1] == 'build' else -1
		TAG = stage['build'][2] if stage['build'][2] == '-t' else -1
		IMAGE_NAME = REPO if stage['build'][3] == 'NAME' else -1
		PATH = ('../' + REPO) if stage['build'][4] == 'REPO' else -1
		if -1 in (DOCKER, BUILD, TAG, IMAGE_NAME, PATH):
			for i in (DOCKER, BUILD, TAG, IMAGE_NAME, PATH): print(i)
			raise ValueError('Invalid Syntax docker-commands.yml BUILD')
	except ValueError as err: print(err)

	try:
		DOCKER = stage['service'][0] if stage['service'][0] == 'docker' else -1
		SERVICE = stage['service'][1] if stage['service'][1] == 'service' else -1
		CREATE = stage['service'][2] if stage['service'][2] == 'create' else -1
		PORT = stage['service'][3] if stage['service'][3] == '-p' else -1
		PORT_NUM = stage['service'][4] if stage['service'][4] != '4000:4000' else -1
		NAME = stage['service'][5] if stage['service'][5] == '--name' else -1
		SERVICE_NAME = REPO if stage['service'][6] == 'SERVICE_NAME' else -1
		IMAGE_NAME = REPO if (stage['service'][7] == 'IMAGE_NAME' and IMAGE_NAME) else -1
		REMOVE = stage['service'][8] if stage['service'][8] == 'rm' else -1
		if -1 in (DOCKER, SERVICE, CREATE, PORT, PORT_NUM, NAME, SERVICE_NAME, IMAGE_NAME, REMOVE):
			for i in (DOCKER, SERVICE, CREATE, PORT, PORT_NUM, NAME, SERVICE_NAME, IMAGE_NAME, REMOVE): print(i)
			raise ValueError('Invalid Syntax docker-commands.yml SERVICE')
	except ValueError as err: print(err)

	SERVICE_NAME = (REPO + '_PRODUCTION') if BRANCH == 'master' else (REPO + '_TEST')		# app_name:production OR app_name:test
	IMAGE_NAME = (IMAGE_NAME + '-prod') if BRANCH == 'master' else (IMAGE_NAME + '-test')

	clients[ready_socket]['production_port'] = PORT_NUM
	clients[ready_socket]['test_port'] = PORT_NUM[:3] + '1:' + PORT_NUM[:4]

	# pull git repo, find port
	PORT_NUM = PORT_NUM if BRANCH == 'master' else clients[ready_socket]['test_port']

	git_checkout = subprocess.check_output(['git', 'checkout', BRANCH],cwd=PATH)
	print('\n' + git_checkout.decode())

	git_pull = subprocess.check_output(['git', 'pull'],cwd=PATH)
	print('\n' + git_pull.decode())


	# docker build PATH -t REPO
	image_build = subprocess.check_output([DOCKER, BUILD, TAG, IMAGE_NAME, PATH], stderr=subprocess.PIPE)
	print('\n' + image_build.decode())


	# docker service create --name NAME REPO
	# first try remove service than create
	try:
		service_rm = subprocess.check_output([DOCKER, SERVICE, REMOVE, SERVICE_NAME], stderr=subprocess.PIPE)
		print('\n' + service_rm.decode())
	except:
		print("\nNo Service to remove")

	service_create = subprocess.check_output([DOCKER, SERVICE, CREATE, PORT, PORT_NUM, NAME, SERVICE_NAME, IMAGE_NAME], stderr=subprocess.PIPE)
	print('\n' + service_create.decode())


	print("Clean Reg:")
	# clean up: remove old builds/images
	image_list = subprocess.check_output(['docker', 'images', '-f', 'dangling=true', '-q'], stderr=subprocess.PIPE)

	for i in (image_list.decode().split('\n')):
            if len(i) is not 0:
                image_to_rm = str(i)
                try:
                    image_rm = subprocess.check_output(['docker', 'image', 'rmi', image_to_rm], stderr=subprocess.PIPE)
                except:
                    print(image_to_rm + " cant be removed: ")
                    pass
	print("\nSUCCESSFULLY AUTO DEPLOY " + REPO + " AT " + PORT_NUM[:4] + "\n")



while True:

		rw = [serversocket]
		rw.extend(clients.keys())
		rw,__,__ = select.select(rw, [], [])

		for ready_socket in rw:
			if ready_socket == serversocket:
				(clientsocket, address) = serversocket.accept()
				clients[clientsocket] = ''
				print("\nserversocket accept!")

			else:
				partial_request = clients[ready_socket]
				data = ready_socket.recv(16384)

				if len(data) == 0:
					# send response to GitHub
					encode_response(ready_socket, 400, 'Bad Request')
					print('Forcing shutdown')
				else:
					request = data.decode("utf-8")
					# update partial http request
					clients[ready_socket] = partial_request + request

					try:
						# webhook: check for valid POST req from GitHub repo
						read_POST(ready_socket)
					except:
						print("POST ERROR:")

					# validate yaml file
					# repo: GitHub evernt that was pushed, repo and branch name
					try:
						read_composefile(ready_socket)
					except Exception as err: print("READ YAML FILE ERROR\n")

					try:
						check_yaml(ready_socket)
					except Exception as err:
						print('Subprocess Error: Check Commands\n')

					encode_response(ready_socket, 200, 'OK')
