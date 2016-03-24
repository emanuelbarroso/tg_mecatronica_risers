
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy
import matplotlib.pyplot as plt

results = numpy.load("data24032016_30cm.npz")
time = results['t']
position = results['position_fundo']
ref_position = 1000*results['ref_position_fundo']

min_dt = time[1] - time[0]
max_dt = min_dt

for i in range(1,len(position)):
	dt = time[i] - time[i-1]
	min_dt = dt if dt < min_dt else min_dt
	max_dt = dt if dt > max_dt else max_dt

print ('min_dt is',min_dt,', max_dt is ',max_dt)
#Tweaks
ref_position[100:] = 300

plt.hold(True)
plt.plot(time,position, label='Actual Position')
plt.plot(time,ref_position, label='Reference Position')
plt.legend()
plt.xlabel('time (s)')
plt.ylabel('position (mm)')
plt.title('Open-Loop Response, 30 cm trajectory')
#show()
plt.savefig('result_30cm.png',dpi=300)
plt.close()
