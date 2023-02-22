# SlipDetection

First install requirements...

Next start the docker container (e.g. with the docker-compose). 
Check the configuration in the redis connector! That may be different...

The mubeaSlipSimulator will create data, vizualize the data within the terminal and write the data into a redis stream

Alert.py read the data from the stream and gives an alert, if a slip occurs
