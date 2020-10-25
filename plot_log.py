#!/usr/bin/python3

import datetime
import sys
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import math

assert len(sys.argv) == 2
filename = sys.argv[1]
v = []
a = []
t = []

with open(filename, 'rb') as lf:
    starttime = datetime.datetime.fromisoformat(lf.readline()[:-1].decode('utf-8'))
    period = int(lf.readline()) / 1000000.0
    resistor = float(lf.readline())
    time = starttime.timestamp()
    print(starttime, period, resistor)
    counter = 0
    while True:
        data = lf.read(6)
        if len(data) < 6:
            break
        assert data[0] == 0xaa
        if data[1] != (counter + 1) and data[1] != 0:
            print('issue with counter')
        counter = data[1]
        bus_raw = int.from_bytes(data[2:4], byteorder='little', signed=True)
        shunt_raw = int.from_bytes(data[4:6], byteorder='little', signed=True)
        print(counter, bus_raw, shunt_raw)
        bus_mv = bus_raw * 1.0
        shunt_mv = shunt_raw * 0.005
        load_mv = bus_mv - shunt_mv
        current_ma = shunt_mv / resistor
        t.append(datetime.datetime.fromtimestamp(time, tz=None))
        v.append(load_mv/1000.0)
        a.append(current_ma)
        time += period

ax_v = plt.figure().add_subplot(111)
ax_v.plot(t, v, color='tab:green')
ax_v.set_ylabel('V', color='tab:green')
ax_v.tick_params(axis='y', labelcolor='tab:green')

ax_a = ax_v.twinx()
ax_a.plot(t, a, color='tab:blue')
ax_a.set_ylabel('mA', color='tab:blue')
ax_a.tick_params(axis='y', labelcolor='tab:blue')

formatter = mdates.DateFormatter("%H:%M:%S.%f")
plt.gca().xaxis.set_major_formatter(formatter)
plt.xlabel('t')
plt.title('Consommation')

ymax = max(a)
ymin = min(a)
plt.ylim((math.floor(ymin), 5 * math.ceil(ymax/5)))
plt.grid(True)

#plt.savefig(filename.replace('log', 'png'), dpi=200)
plt.show()
