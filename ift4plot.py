import numpy as np
import matplotlib.pyplot as plt
import sys
import re

# 0 = time, 1 = vbooster, 2 = vstarship, 3 = hbooster, 4 = hstarship, 5 = abooster, 6 = astarship, 7 = notes
recs = []
for line in sys.stdin:
    fields = re.split(r'\s+', line.strip())
    fields = [None if _=='-' else int(_) for _ in fields[:5]] \
            + [None if _=='-' else float(_) for _ in fields[5:7]] \
            + [ " ".join(fields[7:]) ]
    recs.append(fields)


# Simulated speed data and time intervals
#  time in minutes
#  speed in kmh
#  height in km
tbooster = np.array([r[0]/60 for r in recs if r[1] is not None])
vbooster = np.array([r[1] for r in recs if r[1] is not None])
hbooster = np.array([r[3] for r in recs if r[3] is not None])
abooster = np.array([r[5] for r in recs if r[5] is not None])
tstarship = np.array([r[0]/60 for r in recs if r[2] is not None])
vstarship = np.array([r[2] for r in recs if r[2] is not None])
hstarship = np.array([r[4] for r in recs if r[4] is not None])
astarship = np.array([r[6] for r in recs if r[6] is not None])

# Plot results
fig = plt.figure()
fig.subplots_adjust(wspace=0.08, left=0.1, right=0.85, top=0.95, hspace=0.3, bottom=0.05)

#############
# at the top, the booster plot
axv_b = fig.add_subplot(3, 1, 1)
axv_b.set_title('Booster')
axv_b.set_xlabel('Time [min]')
axv_b.set_ylabel('Velocity (kmh)', color='blue')
axv_b.plot(tbooster, vbooster, color='blue')

# add second y axis
axa_b = axv_b.twinx()
axa_b.set_ylabel('Acceleration [g]', color='red')
axa_b.plot(tbooster, abooster, color='red')

# add third y axis
axh_b = axv_b.twinx()
axh_b.set_ylabel('Height [km]', color='green')
axh_b.plot(tbooster, hbooster, color='green', linestyle=':')
axh_b.spines['right'].set_position(('axes', 1.08))


# starship as one plot, including the coasting part.

axv_s = fig.add_subplot(3, 1, 2)
axv_s.set_title('Starship')
axv_s.set_xlabel('Time [min]')
axv_s.set_ylabel('Velocity (kmh)', color='blue')

axv_s.plot(tstarship, vstarship, color='blue')

# second y axis
axa_s = axv_s.twinx()
axa_s.set_ylabel('Acceleration [g]', color='red')
axa_s.plot(tstarship, astarship, color='red')

# third y axis
axh_s = axv_s.twinx()
axh_s.set_ylabel('Height [km]', color='green')
axh_s.plot(tstarship, hstarship, color='green', linestyle=':')
axh_s.spines['right'].set_position(('axes', 1.08))


#############
# next the starship plot, split in two parts.
# excluding the orbital, coasting part.

# first the launch/boost part

axv_s1 = fig.add_subplot(3, 2, 5)
axv_s1.set_title('Starship (boost)')
axv_s1.set_xlabel('Time [min]')
axv_s1.set_xlim(0, 10)
axv_s1.set_ylabel('Velocity (kmh)', color='blue')

axv_s1.plot(tstarship, vstarship, color='blue')

# second y axis
axa_s1 = axv_s1.twinx()
axa_s1.set_yticks([])
axa_s1.plot(tstarship, astarship, color='red')

# third y axis
axh_s1 = axv_s1.twinx()
axh_s1.set_yticks([])
axh_s1.plot(tstarship, hstarship, color='green', linestyle=':')


#############
# next the descent part

axv_s2 = fig.add_subplot(3, 2, 6)
axv_s2.set_title('Starship (descent)')
axv_s2.set_xlabel('Time [min]')
axv_s2.set_xlim(60, 67)

axv_s2.plot(tstarship, vstarship, color='blue')

axv_s2.set_yticks([])

# second y axis
axa_s2 = axv_s2.twinx()
axa_s2.set_ylabel('Acceleration [g]', color='red')
axa_s2.plot(tstarship, astarship, color='red')

# third y axis
axh_s2 = axv_s2.twinx()
axh_s2.set_ylabel('Height [km]', color='green')
axh_s2.plot(tstarship, hstarship, color='green', linestyle=':')
axh_s2.spines['right'].set_position(('axes', 1.16))

for ax in (axv_s1, axa_s1, axh_s1):
    ax.spines['right'].set_visible(False)
for ax in (axv_s2, axa_s2, axh_s2):
    ax.spines['left'].set_visible(False)

d = .015

kwargs = dict(transform=axv_s1.transAxes, color='k', clip_on=False)
axv_s1.plot((1-d, 1+d), (-d, +d), **kwargs)
axv_s1.plot((1-d, 1+d), (1-d, 1+d), **kwargs)

kwargs.update(transform=axv_s2.transAxes)
axv_s2.plot((-d, +d), (1-d, 1+d), **kwargs)
axv_s2.plot((-d, +d), (-d, +d), **kwargs)


plt.show()


