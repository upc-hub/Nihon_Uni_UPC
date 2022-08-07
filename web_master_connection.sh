#!/bin/bash

web_server_ip=$(jq .web_server[0].IP_address master_worker_info.json)
web_server_ip1="${web_server_ip//'"'}"
echo $web_server_ip1
sshfs root@$web_server_ip1:$PWD/UPC_Web_Server/download/ $PWD/UPC_Master/remove_zip/
sshfs root@$web_server_ip1:$PWD/UPC_Web_Server/results/ $PWD/UPC_Master/results/
sshfs root@$web_server_ip1:$PWD/UPC_Web_Server/status/waiting $PWD/UPC_Master/status/waiting
sshfs root@$web_server_ip1:$PWD/UPC_Web_Server/status/running $PWD/UPC_Master/status/running
sshfs root@$web_server_ip1:$PWD/UPC_Web_Server/status/finished $PWD/UPC_Master/status/finished

docker run -it -v $PWD/UPC_Web_Server/download:/app/download -v $PWD/UPC_Web_Server/results:/app/results -v $PWD/UPC_Web_Server/status:/app/status -p 3000:3000 pollen5005/upc_web_server:latest
