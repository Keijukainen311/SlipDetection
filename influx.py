from datetime import datetime

from influxdb_client.client.write_api import SYNCHRONOUS, ASYNCHRONOUS
from influxdb_client import InfluxDBClient, Point, WritePrecision
import numpy as np
import time

# definitions
mean_velocity_f = 1  # mean velocity of the rolled material exiting the process in m/s
# decreade mean vel r to reduce slip
mean_velocity_r = 0.78  # max velocity of the roll in m/s
max_slip = 0.1  # max slip (delta)
token = "oILj4i_YbXqC768fgCl4Li-FytUl2lqEMJ8QCN4TwwYZPHzTan9CqF-gnbaG0CYNRC-S3TOAtxF4kM-dXdztOQ=="
org = "Mubea"
bucket = "Slip"


class Measurement:
    def __init__(self, f: float, r: float, temperature_machine: float, temperature_material: float):
        self.velocity_f = f
        self.velocity_r = r
        self.date = datetime.now()
        self.temp_machine = temperature_machine
        self.temp_mat = temperature_material

    def __str__(self):
        return "Measurement taken " + self.date.strftime("%m/%d/%Y, %H:%M:%S:%f") + " - velocity_f: " + str(
            self.velocity_f) + " - velocity_r: " + str(self.velocity_r)

    def __repr__(self):
        return str(self)


def simulate_measurement():
    num_r = np.random.default_rng().normal(mean_velocity_r, 0.1, size=None)
    num_f = np.random.uniform(low=max(mean_velocity_f, num_r), high=min(mean_velocity_f, num_r),
                              size=None)  # this could be made more meaningful
    # Generate correlated variables
    temperature_machine = np.random.normal(25, 5)
    temperature_material = np.random.normal(20, 3)
    speed_rolls = (num_f - num_r) * 10 + 100  # linear relation

    m = Measurement(num_f, num_r, temperature_machine,
                    temperature_material)  # , temperature_machine, temperature_material, speed_rolls)
    return m


def simulate_runs(runs: int, delay_ms: int):
    """Simulates simulator runs and stores the results into a InfluxDB."""
    with InfluxDBClient(url=r"http://localhost:8086", token=token, org=org) as client:
        write_api = client.write_api(write_options=ASYNCHRONOUS, write_precision='s')
        for i in range(runs):
            time.sleep(delay_ms / 1000)
            m = simulate_measurement()

            point = Point("mem") \
                .tag("host", "host1") \
                .field("velocity_f", m.velocity_f) \
                .field('velocity_r', m.velocity_r) \
                .field('temperature_machine', m.temp_machine) \
                .field('temperature_material', m.temp_mat) \
                .time(datetime.utcnow(), WritePrecision.NS)
            print(point)
            write_api.write(bucket, org, point)


def main():
    simulate_runs(100, 1000)


if __name__ == '__main__':
    main()
