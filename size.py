import redis_connector
import pandas as pd
from datetime import datetime
import time

r = redis_connector.connect()

"""
size_bytes = r.memory_usage("mubea_trb")
size_mb = round(size_bytes / (1024*1024), 10)
print(size_mb)

"""
# Create an empty df
df = pd.DataFrame(columns=['timestamp', 'size_mb'])

# Loop forever, writing the size of the Redis stream to the df every minute
while True:
    # Get current timestamp...
    now = datetime.now()
    #...in Pretty!
    ts = now.strftime("%Y-%m-%d %H:%M:%S")
    
    # Calculate stream size in megabytes
    size_bytes = r.memory_usage("mubea_trb")
    size_mb = round(size_bytes / (1024*1024), 5)
    print(size_mb)
    # Append new row to df
    df = pd.concat([df, pd.DataFrame({'timestamp': [ts], 'size_mb': [size_mb]})], ignore_index=True)
    
    # Write df to xlsx sheet
    df.to_excel('stream_size.xlsx', index=False)
    
    # Sleep for 1 minute
    time.sleep(60)

