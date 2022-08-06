
from master_operation_openfoam import *


def master_connection_open_close_openfoam(host, port, number, worker_port):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	print ("------------------------------------------")
	print ("Elastic UPC Master is started.")
	try:
		soc.bind((host, int(port)))
	except:
		print ("Bind failed error:"+ str(sys.exc_info()))
		sys.exit()
	soc.listen(120)
	print ("------------------------------------------")
	print ("UPC Master is now listening the workers")
	
	while True:                                                         									#Master automatically issue a thread for the incoming worker
		connection, address = soc.accept()
		ip, port = str(address[0]), str(address[1])
		pc_name = connection.recv(5120).decode("utf8")
		if (pc_name=='PC1'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		elif (pc_name=='PC2'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		elif (pc_name=='PC3'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		elif (pc_name=='PC4'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		elif (pc_name=='PC5'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		elif (pc_name=='PC6'):
			accept_worker(host, connection, ip, pc_name, number, worker_port)
		else:
			print ("There is still no jobs.")

def accept_worker(host, connection, ip, pc_name, number, worker_port):
	try:
		job_flag = 1
		Thread(target=check_job_to_send, args=(host, connection, ip, pc_name, job_flag, number, worker_port)).start()        	#enter to the available worker list, if job exists, worker can accept that job to be processed.Otherwise, keep connected to Master
	except:
		print ("Thread could not start.")
		traceback.print_exc()

def check_job_to_send(host, connection, ip, pc_name, job_flag, number, worker_port):                        					#each worker pc obtains a channel and enter to the available worker list
	print (pc_name+" is connected and plese check jobs.")
	global available_list
	reply = update_worker(pc_name)
	if reply[0]=="No job":
		connection.sendall("wait".encode("utf8"))
	else:
		check_job_to_execute_openfoam(connection, ip, pc_name)