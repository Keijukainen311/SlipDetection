import os
import time
from datetime import datetime
from threading import Timer, Thread

import numpy as np
import plotext as plt

import redis_connector as connector

### definitions
mean_velocity_f = 1  # mean velocity of the rolled material exiting the process in m/s
#decreade mean vel r to reduce slip
mean_velocity_r =  0.78  # max velocity of the roll in m/s
max_slip = 0.1 #max slip (delta)
stream_name = "mubea_trb"


class Measurement:
    def __init__(self, f: float, r: float, temperature_machine: float, temperature_material: float):
        self.velocity_f = f
        self.velocity_r = r
        self.date = datetime.now()
        self.temp_machine = temperature_machine
        self.temp_mat = temperature_material

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
                                                      "temperature_material": str(m.temp_mat)})
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
        num_f = np.random.uniform(low=max(mean_velocity_f, num_r), high=min(mean_velocity_f, num_r), size=None) # this could be made more meaningful
        # Generate correlated variables
        temperature_machine = np.random.normal(25, 5)
        temperature_material = np.random.normal(20, 3)
        speed_rolls = (num_f - num_r) * 10 + 100  #linear relation

        m = Measurement(num_f, num_r, temperature_machine, temperature_material) #, temperature_machine, temperature_material, speed_rolls)
        return m
   #     m = Measurement(num_f, num_r)
    #    return m

    # function executed in a new thread
    def run(self):
        # block for a moment
        time.sleep(self.delay)
        # store data in an instance variable
        self.value = self.simulateMeasurement()

def simulateRuns(runs: int, delay_ms: int, s: MeasurementStore):
    for i in range(runs):
        t = SimulationThread(delay_ms / 1000)
        t.start()
        t.join()
        s.store(t.value)

def monitorRuns(runs: int, d: MeasurementStore, refresh_ms: int):
    labels = []
    velocities_f = []
    velocities_r = []
    delta = []

    values = d.getLast(runs)
    for v in values:
        id, data = v
        labels.append(datetime.strptime(data.get('date'), "%Y-%m-%d %H:%M:%S.%f"))
        velocities_f.append(float(data.get('velocity_f')))
        velocities_r.append(float(data.get('velocity_r')))

        d = float(data.get('velocity_f')) - float(data.get('velocity_r'))
        delta.append(d)

    title = 'Last Runs'
    os.system('cls' if os.name == 'nt' else 'clear')
    plt.clt()
    plt.clf()

    dates = plt.datetimes_to_string(labels)

    # Set the color of each line based on the velocity_f and velocity_r values
    line_color = "red" if velocities_f[-1] < velocities_r[-1] else "blue"
    plt.plot(delta, label="delta", yside="right", fillx=True, color="gray")
    plt.plot(velocities_f, label="f", yside="left", color=line_color)
    plt.plot(velocities_r, label="r", yside="left", color=line_color)

    plt.interactive(True)
    plt.show()

    time.sleep(refresh_ms/1000)

def main():
    client = connector.connect()
    with client:
        client.ping()
        store = MeasurementStore(client, stream_name)
        runs = 500000
        test = Timer(1, simulateRuns, args=(runs, 50, store))
        test.start()
"""
#Raus, weil ich geb einen scheiß auf den Monitor...
        try:
            while True:
                monitorRuns(20, store, 200)

        except KeyboardInterrupt:
            pass
"""
if __name__ == "__main__":
    main()



