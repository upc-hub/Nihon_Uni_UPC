#!/bin/bash
nohup java -jar ./scheduling-0.0.1-SNAPSHOT.jar >logs.log &
echo "----------------------------------------------------------"
echo "****Sam san scheduling API is running at the backgroud****"
echo "----------------------------------------------------------"
python3 ./upc_master_v1.py