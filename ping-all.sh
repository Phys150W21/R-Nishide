#!/bin/bash 

COUNT=0
while [ $COUNT -le 25 ];
do
ping -c 1 192.168.1.${COUNT}
COUNT=$(($COUNT+1))
done 
