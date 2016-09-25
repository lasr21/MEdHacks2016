#!/bin/bash

python hospital.py

cat hospitals.csv

while IFS=, read col1 col2 col3 col4
do
	wget $col2
done < hospitals.csv