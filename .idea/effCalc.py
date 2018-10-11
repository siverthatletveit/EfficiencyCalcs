import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm




# Maxon motor RE50 36V
maxTorque = 1.5                     #[Nm]
maxRPM  = 9000                    #[RPM]
k_n = 77.8                          # Speed constant [rpm/V]
k_T = 0.0604                        # Torque constant [Nm/A]
R = 0.244                           # Winding resistance, DC
I_0 = 0.195                         # No load current; used for calculating friction torque

# Thingap TG3050, Series Y  (https://www.thingap.com/tg305x)
maxTorque = 0.6                     #[Nm]
maxRPM  = 10000                     #[RPM]
V_per_kRPM=6.3                      #[Vpkl-l/kRPM]
k_n = (1/(6.3/1000.0))*np.sqrt(2)   #Speed constant [rpm/V] (converted from [6.3 Vpkl-l/kRPM])
k_T = 0.074  *np.sqrt(3/2)          # Torque constant [Nm/A],
R = 2.027	                        # Winding resistance, DC
#https://www.allaboutcircuits.com/textbook/alternating-current/chpt-10/three-phase-y-delta-configurations/
R=  2.027                         # Winding resistance (LINE) TODO: verify
I_0 = 0.0                         # No load current; not given in datasheet. TODO: Measure

#Alva Thingap
maxTorque = 0.6
maxRPM  = 10000
V_per_kRPM=7.913/6
k_n = (1/(V_per_kRPM/1000.0))*np.sqrt(2)    #Speed constant [rpm/V] (converted from [6.3 Vpkl-l/kRPM])
k_T = 0.16                                  # Torque constant [Nm/A],
R = 2*1/(6/0.26)	                        # star, parallel --> phase resistance #0.0866
I_0 = 0.0                                   # No load current; not given in datasheet. TODO: Measure

#Define torque and speed range
t = np.linspace(0, maxTorque, 500)

radsToRPM =1/(2 * np.pi / 60)
RPMToRads=2 * np.pi / 60
w = np.linspace(0, maxRPM * RPMToRads, 500)  # rad/sec

T, W = np.meshgrid(t, w)
k_w = k_n * 2 * np.pi / 60          # Convert k_n to k_w[rad/s/V]
T_f = I_0 * k_T                     # Friction torque [Nm], which is assumed to be constant over speed
P_m = W * T                         # Mechanical output power [W]
#I = (T + T_f) / k_T                # Motor current [A]

I = T/k_T
print(k_w*k_T)
windingLosses=R*I*I
torqueOut=W*k_T*I
bearingLosses= T_f = I_0 * k_T * W
#EddyCurrentLosses=W*W*0.0003
P_e = windingLosses + torqueOut + bearingLosses  #                 # Electrical power [W]

# P_e=P_e+0.0005*W*W                    #Speed Depending Adjustment
# Motor efficiency
eta_M = P_m / P_e

# h = plt.contourf(W,T,P_e)
# plt.colorbar()
# plt.figure()
# g = plt.contourf(W,T,P_m)
# plt.colorbar()

W_RPM= W*radsToRPM;

plt.figure(figsize=(16, 8))
#plt.set_cmap('gray_r')
plt.contourf(W_RPM, T, eta_M, 40, cmap=cm.gray_r)
plt.colorbar()
CS = plt.contour(W_RPM, T, eta_M, 20, colors='white')
plt.clabel(CS, inline=1, fontsize=10)
plt.title("Efficiency")
plt.xlabel("Speed [RPM]")
plt.ylabel("Torque[Nm]")
