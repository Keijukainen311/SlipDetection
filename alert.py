import redis_connector


def get_alert(r):
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
                m2_velocity_f = fields_dict['m2_velocity_f']
                m2_velocity_r = fields_dict['m2_velocity_r']
                m3_velocity_f = fields_dict['m3_velocity_f']
                m3_velocity_r = fields_dict['m3_velocity_r']
                
                #Give Alert, when slip occurs..
                if velocity_f < velocity_r:
                    print("Slip detected at time ", date, " due to velocity_f < velocity_r")
                
                if m2_velocity_f < m2_velocity_r:
                    print("Slip detected at time ", date, " due to m2_velocity_f < m2_velocity_r")
                
                if m3_velocity_f < m3_velocity_r:
                    print("Slip detected at time ", date, " due to m3_velocity_f < m3_velocity_r")
          
      

if __name__ == "__main__":
    r = redis_connector.connect()
    #entries = r.xrange('mubea_trb', '-', '+') #Give also the results of the stream...
    #get_last_entry(r)
    get_stream_data(r)
    #get_alert(r)
