#!/bin/bash
echo $1
echo $2
docker run -v $1aa:/root/repos/ns-3-allinone/ns-3.30/scratch pollen5005/nssimulator:$2 >& $1aa/results.txt