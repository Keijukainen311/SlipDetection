import redis_connector  

#Read & print Streaming data
def get_stream_data(r):
    while True:
        stream_entries = r.xread({'mubea_trb': '$'}, block=0)

        # process new entries
        for stream in stream_entries:
            for entry_id, fields in stream[1]:
                fields_dict = dict(fields)
                print(fields_dict)
 

def get_last_entry(r):
    result = r.xread({'mubea_trb': '$'}, count=1, block=0)

    if result:
        stream_name, items = result[0]
        last_item = items[0]
        print(last_item)
    else:
        print('Stream is empty')


def get_last_n_entries(r, stream_name, n):
    entries = r.xrevrange(stream_name, count=n)
    return entries


def get_sliding_window(r, stream_name, window_size):
    latest_id = r.xinfo_stream(stream_name)['last-entry'][0]
    entries = r.xrevrange(stream_name, count=window_size)
    oldest_id = entries[-1][0] if entries else latest_id
    window_entries = []
    for id, fields in entries:
        if id >= oldest_id:
            window_entries.append(fields)
    return window_entries

def get_tumbling_window(r, stream_name, window_size):
    latest_id = r.xinfo_stream(stream_name)['last-entry'][0]
    latest_entry_id = latest_id.split("-")[0]
    oldest_id = str(int(latest_entry_id) - (window_size - 1))
    entries = r.xrange(stream_name, oldest_id, latest_id)
    window_entries = []
    for id, fields in entries:
        window_entries.append(fields)
    return window_entries


if __name__ == "__main__":
    r = redis_connector.connect()
    #entries = r.xrange('mubea_trb', '-', '+') #Give also the results of the stream...
    #get_last_entry(r)
    get_stream_data(r)
    
    #last = get_last_n_entries(r, "mubea_trb", 10)

    #slide = get_sliding_window(r, "mubea_trb", 5)
    #print(slide)


    #tumble = get_tumbling_window(r, "mubea_trb", 10)
    #print (tumble)
