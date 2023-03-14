import mubeaSlipSimulator as ms
from datetime import datetime
import os
import plotext as plt


def monitorRuns(runs: int, d: ms.MeasurementStore, refresh_ms: int):
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
