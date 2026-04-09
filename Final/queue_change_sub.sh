#!/bin/bash

for i in $(seq 1691482 1 1691782);do
	scontrol update JobId=$i Partition=mpi
done
