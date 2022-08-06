#!/bin/bash

rm -r $PWD/UPC_Master/remove_zip/*
rm -r $PWD/UPC_Master/results/*
rm -r $PWD/UPC_Master/status/waiting/*
rm -r $PWD/UPC_Master/status/running/*
rm -r $PWD/UPC_Master/status/finished/*

umount $PWD/UPC_Master/remove_zip/
umount $PWD/UPC_Master/results/
umount $PWD/UPC_Master/status/waiting
umount $PWD/UPC_Master/status/running
umount $PWD/UPC_Master/status/finished

