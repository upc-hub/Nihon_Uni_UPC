import socket
import sys, os
import datetime
import time
import subprocess
import csv
global counter
from threading import Thread

def static_client_main1(host, port):
	print ("----------------------------------------")
	print ("----------------------------------------")
	print (host, "******", port)
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	try:
		soc.bind((host, port))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
	soc.listen(2)
	while True:
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		print ("A master node connected with "+ip+" : "+port)
		time.sleep(5)
		message = connection.recv(5120).decode("utf8")
		print ("----------------------------------------")
		print (message)
		print ("----------------------------------------")

if __name__ == "__main__":
	static_client_main1('172.28.235.202', 1600)