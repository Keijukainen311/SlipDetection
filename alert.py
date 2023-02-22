import redis_connector


def get_stream_data(r):
    while True:
        stream_entries = r.xread({'mubea_trb': '$'}, block=0)

        # process new entries
        for stream in stream_entries:
            for entry_id, fields in stream[1]:
                
                fields_dict = dict(fields)
                #print(fields_dict)
                date = fields_dict['date']
                velocity_f = fields_dict['velocity_f']
                velocity_r = fields_dict['velocity_r']
                if velocity_f < velocity_r:
                    print("slip at time ", date)
                #print(fields_dict)



def get_last_data(r):
    result = r.xread({'mubea_trb': '$'}, count=1, block=0)

    if result:
        stream_name, items = result[0]
        last_item = items[0]
        print(last_item)
    else:
        print('Stream is empty')


if __name__ == "__main__":
    r = redis_connector.connect()
    #entries = r.xrange('mubea_trb', '-', '+')
    #get_last_data(r)
    get_stream_data(r)

