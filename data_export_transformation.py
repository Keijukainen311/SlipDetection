import redis_connector as connector
import pandas as pd
import numpy as np
import seaborn as sb
import time

r = connector.connect()

# Set the timestamp range
start_timestamp = int(time.time() - 3600) * 1000 # 1 hour ago in milliseconds
end_timestamp = int(time.time()) * 1000 # current time in milliseconds

# Create data frame 
stream_data_df=pd.DataFrame(columns=['date','velocity_f','velocity_r','temperature_machine','temperature_material'])

# Query the stream for messages within the timestamp range
stream_entries = r.xrange('mubea_trb',start_timestamp, end_timestamp)

# Tranform new entries and append to data frame
for stream in stream_entries:
    df=pd.DataFrame(stream[1], index=[stream[0]])
    stream_data_df=pd.concat([stream_data_df,df])
    fields_dict = dict(stream[1])
   
  
# Change data types
stream_data_df['date']=stream_data_df['date'].astype({'date': 'datetime64[ns]'})
stream_data_df['velocity_f']=stream_data_df['velocity_f'].astype(float)
stream_data_df['velocity_r']=stream_data_df['velocity_r'].astype(float)
stream_data_df['temperature_machine']=stream_data_df['temperature_machine'].astype(float)
stream_data_df['temperature_material']=stream_data_df['temperature_material'].astype(float)

print(len(stream_data_df))

# Calculate new columns
stream_data_df['delta_velocity_f_velocity_r']=stream_data_df['velocity_f']-stream_data_df['velocity_r']

# Calculate correlation between numeric columns
cols=stream_data_df.select_dtypes([np.number]).columns
cm = np.corrcoef(stream_data_df[cols].values.T)
hm = sb.heatmap(cm, annot=True,cmap="YlGnBu",xticklabels=cols,yticklabels=cols)


