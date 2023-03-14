# SlipDetection

## Run container
Go to this directory and run
```
docker-compose up
```
Or run the container by hand...

## Start Simulating Data

First install requirements..
```
pip install requirements.txt
```

Check the configuration in the **redis_connector.py**! That may be different, to the settings in this script!

The ***mubeaSlipSimulator.py** will create data, **monitor.py** vizualize the data within the terminal and write the data into a redis stream.

**alert.py** read the data from the stream and gives an alert, if a slip occurs

**get_Data.py** has different functions to read data from the stream (print the stream, print the last values, print different windows)

**size.py** displays the size of the redis instance within a specific time period and wirte it into a excel file.


## Grafana configuration
Make sure the Redis Plugin is installed
If u are using this docker-compose the redis plugins are already installed, otherwise install it manually:
Settings -> Plugin -> Redis -> redis-datasource & redis-app

Connect to redis
Now choose the redis-datasource and create a new data source. 
There are different ways to connect to the redis data source (as) sometimes the address don't work properly..):
- localhost:6379 (or whatever port your redis instance is using...)
- IP-Address mentioned in the Docker-Compose : Port of redis instance 
- host.docker.internal:Port of redis instance
- Run in commandline: docker run --rm alpine nslookup host.docker.internal
and use the ip address mentioned then...

The connection is now running. You can create different kind of 