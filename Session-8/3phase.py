
import matplotlib.pyplot as plt
import math
v_peak = 311.12
f = 50
pi = 3.14159
period = 0.04  
t_data = []
p1_data = []
p2_data = []
p3_data = []

points = 500
for i in range(points):

    t = (period * i) / points 
    t_data.append(t)

    v1 = v_peak * math.sin(2 * pi * f * t)
    v2 = v_peak * math.sin(2 * pi * f * t - (2 * pi / 3))
    v3 = v_peak * math.sin(2 * pi * f * t - (4 * pi / 3))

    p1_data.append(v1)
    p2_data.append(v2)
    p3_data.append(v3)

plt.figure(figsize=(10, 6))
plt.plot(t_data, p1_data, color='red', label='L1 (R)')
plt.plot(t_data, p2_data, color='gold', label='L2 (S)')
plt.plot(t_data, p3_data, color='blue', label='L3 (T)')

plt.axhline(0, color='black', linewidth=1)
plt.title('3-Phase Voltage Graph')
plt.xlabel('Time (s)')
plt.ylabel('Voltage (V)')
plt.grid(True, alpha=0.3)
plt.legend()
plt.show()