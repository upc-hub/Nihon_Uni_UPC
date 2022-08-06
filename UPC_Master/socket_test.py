import socket
import sys
import time

def worker_connect(host, port, message):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host,int(port)))
	except:
		print ("Connection error")
		sys.exit()
	time.sleep(5)
	soc.sendall(message.encode("utf8"))

if __name__ == "__main__":
	worker_connect('172.28.235.202', 1600, "***************Prepare to accept migrated job****************")