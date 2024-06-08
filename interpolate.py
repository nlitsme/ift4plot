import sys
import re

"""
 - makes sure there is an entry for every second
 - fills in the blanks by doing linear interpolation between known values.
"""

previx = None
recs = []
for line in sys.stdin:
    r = re.split(r'\s+', line.strip())
    r = [None if _=='-' else int(_) for _ in r[:6]] + r[6:]
    ix = r[0]
    if previx is not None and ix-previx > 1:
        for i in range(previx+1, ix):
            recs.append([i] + [None]*5)
    recs.append(r)
    previx = ix

def interpolate_t():
    previ = None
    prevt = None
    count = 0
    for i, r in enumerate(recs):
        t = r[1]
        if t is None:
            count += 1
        else:
            if count:
                #  ft(previ) = prevt
                #  ft(i)   = t
                at = (t-prevt)/(i-previ)
                bt = (i*prevt-previ*t)/(i-previ)
                ft = lambda i:at*i+bt

                for j in range(previ+1, i):
                    recs[j][1] = round(ft(j))

            previ = i
            prevt = t


def interpolate(c):
    previ = None
    prevv = None
    count = 0
    for i, r in enumerate(recs):
        t = r[1]
        v = r[c]
        if v is None:
            count += 1
        else:
            if count:
                #  ft(previ) = prevt
                #  ft(i)   = t
                at = (t-prevt)/(i-previ)
                bt = (i*prevt-previ*t)/(i-previ)
                ft = lambda i:at*i+bt

                #  fv(prevt) = prevv
                #  fv(t)     = v
                a = (v-prevv)/(t-prevt)
                b = (t*prevv-prevt*v)/(t-prevt)
                fv = lambda t:a*t+b
                for j in range(previ+1, i):
                    recs[j][c] = round(fv(recs[j][1]))
                    if abs(recs[j][1] - ft(j)) > 0.1:
                        print("!!", j, "->", ft(j), "!=", recs[j][1])

            previ = i
            prevt = t
            prevv = v

interpolate_t()
for c in range(2, 6):
    interpolate(c)

for r in recs:
    print("".join(f"%9s" % ("-" if _ is None else _) for _ in r[:6]), "   ", " ".join(r[6:]))
