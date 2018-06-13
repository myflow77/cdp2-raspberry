# -*- coding: utf-8 -*-

# Socket
from socket import *
from select import *
import sys
from time import ctime
# Multiprocess
import threading
import time
from queue import Queue
# Json
import json

def run():
	#HOST = '211.202.32.174'
	HOST = '127.0.0.1'
	PORT = 9999
	BUFSIZE = 1024
	ADDR = (HOST, PORT)

	clientSocket = socket(AF_INET, SOCK_STREAM)  # 1 서버에 접속하기 위한 소켓을 생성한다.

	clientSocket.connect(ADDR)  # 2. 서버에 접속을 시도한다.
	print('connect is success')

	'''
	class Receive(threading.Thread):
		def run(self):
			self.alive = True
			# 하위 프로세스(기능)에서 수신된 메세지를 디바이스에 전달
			while(self.alive):
				message = clientSocket.recv(BUFSIZE).decode('utf-8')
				if (message == 'quit'):
					break
				elif (message != ''):
					print(message)

		def stop(self):
			self.alive = False
			self.join()

	receive = Receive()
	receive.daemon = True
	receive.start()
	'''

	while(True):
		command = input("Command Number : ")

		dic = {}
		# 커맨드에 따라 명령을 생성
		if command == '0':
			print("Command 0")
			dic['message'] = 'list'
		elif command == '1':
			print("Command 1")
			dic['message'] = 'delete'
			dic['filename'] = 'ChillingMusic.1.wav'
		elif command == '2':
			print("Command 2")
			dic['message'] = 'play'
			dic['filename'] = 'ChillingMusic.wav'
		elif command == '3':
			# 파일 전송 - 미구현
			pass
		elif command == 'quit':  # 종료 명령이 들어왔을 경우
			print("Device is stopping")
			#receive.stop()
			sys.exit(0)
			print('Device closed')
			break

		# 명령을 json으로 변환
		json_str = json.dumps(dic)

		# 변환된 명령을 기기로 전송
		clientSocket.send(json_str.encode('utf-8'))

		# 특정 명령의 경우 결과를 반환받음
		if command == '0':
			json_str = clientSocket.recv(BUFSIZE).decode('utf-8')
			try:
				json_data = json.loads(json_str)
				files = json_data['files']
				print(files)
			except Exception as e:
				print(e)

	print('Device is closed')


# [START] main
if __name__ == "__main__":
	run()
# [END] main
