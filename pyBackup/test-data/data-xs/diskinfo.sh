#!/bin/bash

for x in /sys/block/sd*
do
	echo -e "/dev/$dev \t ata$a.$a2 \t $model \t $serial"
done;
