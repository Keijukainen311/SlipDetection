import redis_connector

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

r = redis_connector.connect()
#last = get_last_n_entries(r, "mubea_trb", 10)

slide = get_sliding_window(r, "mubea_trb", 5)
#print(slide)


tumble = get_tumbling_window(r, "mubea_trb", 10)
print (tumble)