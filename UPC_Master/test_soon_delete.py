import time

def migrate_call():
	worker_free_not = [0,0,0,1,0,1]
	worker_name = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6']
	available = []
	available_index = []
	busy = []
	global busy_index
	busy_index = []
	suitable = []
	selected = []
	for i, e in enumerate(worker_free_not): 
		if e == 0:
			#print (e, '***', i)
			available.append(e)
			available_index.append(i)
		else:
			busy.append(e)
			busy_index.append(i)
			#print (e, '<>', i)

	#print ("Available worker", available)
	print ("Available worker index ", available_index)
	#print ("Busy worker", busy)
	print ("Busy worker index", busy_index)


	for a in range(len(available_index)):
		for i in range(len(busy_index)):
			if busy_index[i]<available_index[a]:
				suitable.append(busy_index[i])
		#print (suitable)
		selected.append(min(suitable))
		#print (busy_index)
		del busy_index[0:len(suitable)]
		#print ("b", busy_index)
		for j in range(len(suitable)):
			suitable.pop(0)
		#print (suitable)
	print (selected)
		



	#print (worker_free_not)
	#print ("Migration is started.........")
	#index = 0
	#for suitable_worker in worker_free_not:
	#	if suitable_worker==0:
	#		index = index + 1
	#		break
	#	else:
	#		index = index + 1
	
	#print (worker_free_not[index-1])
	#print (worker_free_not)
	#for suitable_worker in worker_free_not[0:index-1]:
	#	print (suitable_worker)
def checking():
	worker_free_not = [0,0,0,0,1,0]
	worker_name = ['PC1', 'PC2', 'PC3', 'PC4', 'PC5', 'PC6']
	source_worker, destination_worker = [], []
	busy = '1'
	free = '0'
	not_working = '2'

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
	print ("Free", available_status,"PC --->", available_index)
	print ("Busy", busy_status,"PC --->", busy_index)
	print ("Not working", no_working_status,"PC --->", no_working_index)
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
	
	print ("Source", selected_name, 'Destination', selected)
	for aa in selected_name:
		source_worker.append(worker_name[aa])
	for aa in selected:
		destination_worker.append(worker_name[aa])

	print ("Source", source_worker, "Destination", destination_worker)

if __name__ == "__main__":
	checking()