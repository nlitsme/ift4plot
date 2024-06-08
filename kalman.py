import numpy as np
import matplotlib.pyplot as plt
import sys
import re

# 0 = fnum, 1 = time, 2 = vbooster, 3 = vstarship, 4 = hbooster, 5 = hstarship
recs = []
for line in sys.stdin:
    fields = re.split(r'\s+', line.strip())
    fields = [None if _=='-' else int(_) for _ in fields[:6]] + [ 0, 0 ] + fields[6:]
    recs.append(fields)


# Simulated speed data and time intervals
#  time in minutes
#  speed in m/s
tbooster = np.array([r[1]/60 for r in recs if r[2] is not None])
vbooster = np.array([r[2]/3.6 for r in recs if r[2] is not None])
tstarship = np.array([r[1]/60 for r in recs if r[3] is not None])
vstarship = np.array([r[3]/3.6 for r in recs if r[3] is not None])

def kalman(vmeas):
    # Kalman filter parameters
    delta_t = 1
    F = np.array([[1, delta_t], [0, 1]])  # State transition matrix
    H = np.array([[1, 0]])  # Measurement matrix
    Q = np.array([[1, 0], [0, 1]]) * 0.01  # Process noise covariance
    R = np.array([[1]]) * 0.5  # Measurement noise covariance

    # Initial estimates
    x = np.array([0, 0])  # Initial state (velocity and acceleration)
    P = np.eye(2)  # Initial covariance

    # Storage for results
    estimated_velocities = []
    estimated_accelerations = []

    # Kalman filter implementation
    for z in vmeas:
        # Prediction
        x = F @ x
        P = F @ P @ F.T + Q
        
        # Measurement update
        K = P @ H.T @ np.linalg.inv(H @ P @ H.T + R)
        x = x + K @ (z - H @ x)
        P = (np.eye(2) - K @ H) @ P
        
        # Store estimates
        # convert speed to kmh
        # convert accel to g
        estimated_velocities.append(x[0]*3.6)
        estimated_accelerations.append(x[1]/9.81)

    return  estimated_velocities, estimated_accelerations

vstarship, astarship = kalman(vstarship)
vbooster, abooster = kalman(vbooster)

# Plot results
fig = plt.figure()
fig.subplots_adjust(wspace=0.08)

#############
# at the top, the booster plot
axv_b = fig.add_subplot(2, 1, 1)
axv_b.set_title('Booster')
axv_b.set_xlabel('Time [min]')
axv_b.set_ylabel('Velocity (kmh)', color='blue')
axv_b.plot(tbooster, vbooster, label='speed', color='blue')
axa_b = axv_b.twinx()
axa_b.set_ylabel('Accel [g]', color='red')
axa_b.plot(tbooster, abooster, label='accel', color='red')

#############
# next first starship plot

axv_s1 = fig.add_subplot(2, 2, 3)
axv_s1.set_title('Starship')
axv_s1.set_xlabel('Time [min]')
axv_s1.set_xlim(0, 10)
axv_s1.set_ylabel('Velocity (kmh)', color='blue')

axv_s1.plot(tstarship, vstarship, label='speed', color='blue')

axa_s1 = axv_s1.twinx()
axa_s1.tick_params(axis='y', which='both', right=False, labelright=False)
axa_s1.plot(tstarship, astarship, label='accel', color='red')

#############
# second startship plot

axv_s2 = fig.add_subplot(2, 2, 4, sharey=axv_s1)
axv_s2.set_title('Starship')
axv_s2.set_xlabel('Time [min]')
axv_s2.set_xlim(45, 67)

axv_s2.plot(tstarship, vstarship, label='speed', color='blue')

# TODO: this somehow does not remove the tickmarks.
axv_s2.tick_params(axis='y', which='both', left=False, labelleft=False)
axv_s2.yaxis.set_ticks_position('none')

axa_s2 = axv_s2.twinx()
axa_s2.set_ylabel('Accel [g]', color='red')
axa_s2.plot(tstarship, astarship, label='accel', color='red')

#axa_s1.spines['right'].set_visible(False)
#axv_s1.spines['right'].set_visible(False)
#axa_s2.spines['left'].set_visible(False)
#axv_s2.spines['left'].set_visible(False)

plt.show()

