import time
from threading import Timer, Thread

import numpy as np

import redis_connector as connector
import monitorTerminal

### definitions
mean_velocity_f = 1  # mean velocity of the rolled material exiting the process in m/s
#decreade mean vel r to reduce slip
mean_velocity_r =  0.7  # max velocity of the roll in m/s
max_slip = 0.1 #max slip (delta)
stream_name = "mubea_trb"

class Measurement:
    def __init__(self, f: float, r: float, temperature_machine: float, temperature_material: float, m2_f: float, m2_r: float, m3_f: float, m3_r: float):
        self.velocity_f = f
        self.velocity_r = r
        self.date = datetime.now()
        self.temp_machine = temperature_machine
        self.temp_mat = temperature_material
        self.m2_velocity_f = m2_f
        self.m2_velocity_r = m2_r
        self.m3_velocity_f = m3_f
        self.m3_velocity_r = m3_r

    def __str__(self):
        return "Measurement taken " + self.date.strftime("%m/%d/%Y, %H:%M:%S:%f") + " - velocity_f: " + str(self.velocity_f) + " - velocity_r: " + str(self.velocity_r)

    def __repr__(self):
        return str(self)

class MeasurementStore(object):
    def __new__(cls, redisClient: object, streamName: str):
        if not hasattr(cls, 'instance'):
            cls.instance = super(MeasurementStore, cls).__new__(cls)
        return cls.instance

    def __init__(self, redisClient: object, streamName: str):
        self._redisClient = redisClient
        self._streamName = streamName

    def store(self, m: Measurement):
        with self._redisClient:
            self._redisClient.xadd(self._streamName, {"date": str(m.date), "velocity_f": str(m.velocity_f),
                                                      "velocity_r": str(m.velocity_r), "temperature_machine": str(m.temp_machine),
                                                      "temperature_material": str(m.temp_mat), "m2_velocity_f": str(m.m2_velocity_f),
                                                      "m2_velocity_r": str(m.m2_velocity_r), "m3_velocity_f": str(m.m3_velocity_f),
                                                      "m3_velocity_r": str(m.m3_velocity_r)
                                                      })
            return True
        return False

    def getLast(self, count: int):
        with self._redisClient:
            l = self._redisClient.xlen(self._streamName)

            if l > 0:
                values = self._redisClient.xrevrange(self._streamName, min='-', max='+',
                                                     count=min(l, count))  # getting the last elements from stream
                values.reverse()  # reversing for better plot
                return values
        return []


# custom thread to run simulation and store to Redis
class SimulationThread(Thread):
    # constructor
    def __init__(self, delay: float):
        # execute the base constructor
        Thread.__init__(self)
        # set the delay for run
        self.delay = delay
        # set a default value
        self.value = None

    def simulateMeasurement(self):
        num_r = np.random.default_rng().normal(mean_velocity_r, 0.1, size=None)
        num_f = np.random.uniform(low=max(mean_velocity_f, num_r), high=min(mean_velocity_f, num_r + max_slip), size=None) 
        m2_num_r = np.random.default_rng().normal(mean_velocity_r, 0.1, size=None)
        m2_num_f = np.random.uniform(low=max(mean_velocity_f, m2_num_r), high=min(mean_velocity_f, m2_num_r + max_slip), size=None) 
        m3_num_r = np.random.default_rng().normal(mean_velocity_r, 0.1, size=None)
        m3_num_f = np.random.uniform(low=max(mean_velocity_f, m3_num_r), high=min(mean_velocity_f, m3_num_r + max_slip), size=None) 

        # Generate correlated variables
        temperature_machine = np.random.normal(25, 1)
        temperature_material = np.random.normal(20, 1)
        speed_rolls = (num_f - num_r) * 10 + 100  #linear relation

        m = Measurement(num_f, num_r, temperature_machine, temperature_material, m2_num_f, m2_num_r, m3_num_f, m3_num_r) 
        return m

    # function executed in a new thread
    def run(self):
        # block for a moment
        time.sleep(self.delay)
        # store data in an instance variable
        self.value = self.simulateMeasurement()

def simulateRuns(runs: int, delay_ms: int, s: MeasurementStore):
    for i in range(runs):
        t = SimulationThread(delay_ms) # / 1000) #hier zu Demo Zwecke etwas runter gesetzt....
        t.start()
        t.join()
        s.store(t.value)

def main():
    client = connector.connect()
    with client:
        client.ping()
        store = MeasurementStore(client, stream_name)
        runs = 500000
        test = Timer(1, simulateRuns, args=(runs, 1, store)) # hier den Delay von 50 auf 1 gesetzt...
        test.start()

"""
#Dont want the monitor right now...
        try:
            while True:
                monitorTerminal.monitorRuns(20, store, 200)

        except KeyboardInterrupt:
            pass
"""

if __name__ == "__main__":
    main()



