import time
import json
import socket
import sys
import shutil
import multiprocessing
from threading import Thread

def migrate_call(worker_free_not):
	worker_name = ['worker-1', 'worker-2', 'worker-3', 'worker-4', 'worker-5', 'worker-6']
	source_worker, destination_worker = [], []
	busy = '1'
	free = '0'
	not_working = '2'
	worker1 = worker_free_not[0]
	worker2 = worker_free_not[1]
	worker3 = worker_free_not[2]
	worker4 = worker_free_not[3]
	worker5 = worker_free_not[4]
	worker6 = worker_free_not[5]

	available_status, available_index = [], []
	busy_status, busy_index = [], []
	no_working_status, no_working_index = [], []
	selected, selected_name = [], []
	for i, e in enumerate(worker_free_not): 
		if e == 0:
			available_status.append(e)
			available_index.append(i)
		elif e == 1:
			busy_status.append(e)
			busy_index.append(i)
		else:
			no_working_status.append(e)
			no_working_index.append(i)

	available_status.sort(reverse=True)
	available_index.sort(reverse=True)
	#print ("Free", available_status,"PC --->", available_index)
	#print ("Busy", busy_status,"PC --->", busy_index)
	#print ("Not working", no_working_status,"PC --->", no_working_index)
	try:
		for ava in range(len(available_index)):
			try:
				selected_name.append(min(busy_index))
				busy_index.remove(min(busy_index))
				selected.append(available_index[ava])
			except ValueError:
				break
	except IndexError:
		print ("Done.")
	
	remove_index_imposiible_migrate_src = []
	remove_index_imposiible_migrate_des = []
	for cc in range(len(selected_name)):
		print (selected_name[cc], selected[cc])
		if (int(selected[cc])>int(selected_name[cc])):
			print ("Source", selected_name[cc], 'Destination', selected[cc])
			print ("It is okay to migrate.")
		else:
			print ("Source", selected_name[cc], 'Destination', selected[cc])
			print ("Not okay to migrate.")
			remove_index_imposiible_migrate_src.append(selected_name[cc])
			remove_index_imposiible_migrate_des.append(selected[cc])
	
	for src in remove_index_imposiible_migrate_src:
		selected_name.remove(src)

	for des in remove_index_imposiible_migrate_des:
		selected.remove(des)

	for aa in selected_name:
		source_worker.append(worker_name[aa])
	for aa in selected:
		destination_worker.append(worker_name[aa])

	for srcc in source_worker:
		if srcc=="worker-1":
			worker1 = 0
		elif srcc=="worker-2":
			worker2 = 0
		elif srcc=="worker-3":
			worker3 = 0
		elif srcc=="worker-4":
			worker4 = 0
		elif srcc=="worker-5":
			worker5 = 0
		else:
			worker6 = 0

	for srcc in destination_worker:
		if srcc=="worker-1":
			worker1 = 1
		elif srcc=="worker-2":
			worker2 = 1
		elif srcc=="worker-3":
			worker3 = 1
		elif srcc=="worker-4":
			worker4 = 1
		elif srcc=="worker-5":
			worker5 = 1
		else:
			worker6 = 1
	source_worker_host, source_worker_port, destination_worker_host, destination_worker_port, source_message, destination_message = '',0,'',0,'',''
	print ("Source", source_worker, "Destination", destination_worker)
	# for contact in source_worker:
	# 	source_worker_host, source_worker_port = send_migrate_info_to_worker(str(contact))
	# 	print ("Host", source_worker_host, "port", source_worker_port)
	# 	source_message = "***************Stop Current running job****************"
	# 	worker_connect(source_worker_host, source_worker_port, source_message)

	# for contact in destination_worker:
	# 	destination_worker_host, destination_worker_port = send_migrate_info_to_worker(str(contact))
	# 	print ("Host", destination_worker_host, "port", destination_worker_port)
	# 	destination_message = "***************Prepare to accept migrated job****************"
	# 	worker_connect(destination_worker_host, destination_worker_port, destination_message)

	for i in range(len(source_worker)):
		source_pc = source_worker[i]
		destination_pc = destination_worker[i]
		#print (source_pc, destination_pc)
		source_worker_host, source_worker_port = send_migrate_info_to_worker(str(source_pc))
		print ("Host", source_worker_host, "port", source_worker_port)
		source_message = "stop"
		destination_worker_host, destination_worker_port = send_migrate_info_to_worker(str(destination_pc))
		print ("Host", destination_worker_host, "port", destination_worker_port)
		destination_message = "prepare"
		stop_msg = Thread(target = worker_connect, args = (source_worker_host, source_worker_port, source_message, destination_pc))
		prepare_msg = Thread(target = worker_connect1, args = (destination_worker_host, destination_worker_port, destination_message, source_pc))
		stop_msg.start()
		prepare_msg.start()

	return worker1, worker2, worker3, worker4, worker5, worker6

def send_migrate_info_to_worker(worker_migrate):
	file = './master_worker_info.json'
	worker_ip = ''
	worker_port = ''
	with open(file) as json_file:
		data = json.load(json_file)
		for worker in data[worker_migrate]:
			worker_ip = worker['IP_address']
			worker_port = worker['port2']
	return worker_ip, worker_port

def worker_connect(host, port, message, pc_name):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host,int(port)))
	except:
		print ("Connection error")
		sys.exit()
	time.sleep(5)
	soc.sendall(message.encode("utf8"))
	time.sleep(5)
	soc.sendall(pc_name.encode("utf8"))
	time.sleep(5)
	move_container_master = soc.recv(5120).decode("utf8")
	detect_pc_move = move_container_master.split("_")
	#print (detect_pc_move)
	if detect_pc_move[2]=="stop":
		print (detect_pc_move)
		#shutil.move('./'+detect_pc_move[3]+'/'+detect_pc_move[0]+'_'+detect_pc_move[1],'./'+detect_pc_move[4]+'/')
	else:
		print ("Job doesn't need to move.")

def worker_connect1(host, port, message, pc_name):
	soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		soc.connect((host,int(port)))
	except:
		print ("Connection error")
		sys.exit()
	time.sleep(5)
	soc.sendall(message.encode("utf8"))
	time.sleep(5)
	soc.sendall(pc_name.encode("utf8"))
	time.sleep(5)
	move_container_master = soc.recv(5120).decode("utf8")
	detect_pc_move = move_container_master.split("_")
	print (detect_pc_move)
	if detect_pc_move[2]=="stop":
		print (detect_pc_move)
		#shutil.move('./'+detect_pc_move[3]+'/'+detect_pc_move[0]+'_'+detect_pc_move[1],'./'+detect_pc_move[4]+'/')
	else:
		print ("Job doesn't need to move.")

#if __name__ == "__main__":
#	worker_free_not = [2,2,2,2,1,0]
#	migrate_call(worker_free_not)
