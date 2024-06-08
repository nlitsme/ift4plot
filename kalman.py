import numpy as np
import sys
import re

"""
outputs estimations for the actual velocity, and acceleration.
calculated using a kalman filter.
"""

# 0 = fnum, 1 = time, 2 = vbooster, 3 = vstarship, 4 = hbooster, 5 = hstarship
recs = []
for line in sys.stdin:
    fields = re.split(r'\s+', line.strip())
    fields = [None if _=='-' else int(_) for _ in fields[:6]] \
            + [ " ".join(fields[6:]) ]
    recs.append(fields)


#  time in minutes
#  speed in m/s
#  height in km
vbooster = np.array([r[2]/3.6 for r in recs if r[2] is not None])
hbooster = np.array([r[4] for r in recs if r[4] is not None])
tstarship = np.array([r[1] for r in recs if r[3] is not None])
vstarship = np.array([r[3]/3.6 for r in recs if r[3] is not None])
hstarship = np.array([r[5] for r in recs if r[5] is not None])
notes = [r[6] for r in recs]

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

# pad the booster columns with 'None', so the 'zip' will output full data for all items.
nones = [None]*(len(vstarship)-len(vbooster))
vbooster = list(vbooster) + nones
abooster = list(abooster) + nones
hbooster = list(hbooster) + nones

for fields in zip(tstarship, vbooster, vstarship, hbooster, hstarship, abooster, astarship, notes, strict=True):
    print("".join("        -" if x is None else f"{x:>9.0f}" for x in fields[:5]), end="")
    print("".join("        -" if x is None else f"{x:>9.4f}" for x in fields[5:7]), end="")
    print("   ", fields[7])

