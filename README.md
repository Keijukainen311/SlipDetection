# SlipDetection

First install requirements...

Next start the docker container (e.g. with the docker-compose). 
Check the configuration in the redis connector! That may be different...

The mubeaSlipSimulator will create data, vizualize the data within the terminal and write the data into a redis stream

Alert.py read the data from the stream and gives an alert, if a slip occurs


## Grafana configuration
Einrichtung der Verbindung
Einstellungen -> Plugin -> Redis -> ggf. installieren, ist bereits installiert wenn die Docker Compose von hier genutzt wurde -> Create Data Source
Hier muss die Adresse und das Password gesetzt werden. Entweder analog zur Docker Compose hier oder wie selbst gesetzt.

Grafana hat z.T. Probleme sich mit Redis zu verbinden. Die Adresse kann sein: 
- localhost:6379
- IP-Adresse der Docker Compose : Port 
- host.docker.internal:6379

Danach können Dashboards mit den Daten erstellt werden
