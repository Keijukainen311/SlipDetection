import redis_connector as connector


r = connector.connect()

# Define stream name
stream_name = 'mubea_trb'

# Define stream offset
stream_offset = '$'

# Listen to stream and print new entries
while True:
    stream_data = r.xread({stream_name: stream_offset}, count=1, block=0)
    if stream_data:
        # Get the message ID and data from the first (and only) entry in the stream
        message_id, message_data = stream_data[0][1][0]
        print(f'Message ID: {message_id}')
        print(f'Message data: {message_data}')