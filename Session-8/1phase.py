import matplotlib.pyplot as plt
import math

v_rms = 155
v_peak = v_rms * math.sqrt(2) 
frequency = 50
period = 1 / frequency
t_list = []
v_list = []
points = 1000

for i in range(points):
    t = (2 * period) * (i / points)
    v = v_peak * math.sin(2 * math.pi * frequency * t)
    t_list.append(t)
    v_list.append(v)
plt.figure(figsize=(10, 5))
plt.plot(t_list, v_list, color='blue', label='Voltage (V)')
plt.axhline(y=v_peak, color='red', linestyle='--', label=f'Peak: {v_peak:.1f}V')
plt.axhline(y=-v_peak, color='red', linestyle='--')
plt.axhline(y=0, color='black', linewidth=1) 
plt.title('Iran City Power Grid Voltage (220V RMS, 50Hz)')
plt.xlabel('Time (seconds)')
plt.ylabel('Voltage (Volts)')
plt.grid(True, linestyle=':', alpha=0.6)
plt.legend()

plt.show()