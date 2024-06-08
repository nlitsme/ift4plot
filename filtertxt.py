import sys
import re
"""
reads the uneditted OCR output, and tries to extract any thing which looks like:
    - a time stamp
    - a speed
    - an altitude
"""

def main():
    frames = []
    f = None

    for line in sys.stdin:
        line = line.lower().strip()
        found = []
        if m := re.match('== f/output_(\d+)\.png', line):
            f = {'framenr':int(m[1])}
            frames.append(f)
            found.append('f')

        if m := re.search('t([+-])(\d\d):(\d\d):(\d\d)', line):
            t = int(m[2])*3600+int(m[3])*60+int(m[4])
            if m[1]=='-':
                t = -t
            f['t'] = t
            found.append('t')

        if m := re.search('speed\s*(\d+)\s*k.*?speed\s*(\d+)\s*k', line):
            f['speed1'] = int(m[1])
            f['speed2'] = int(m[2])
            found.append('s1')
            found.append('s2')
        elif m := re.search('speed\s*(\d+)\s*k', line):
            if 'speed2' in f:
                f['speed1'] = int(m[1])
                found.append('s1')
            else:
                f['speed2'] = int(m[1])
                found.append('s2')
        elif m := re.search('(\d+)\s*km.h', line):
            if 'speed2' in f:
                f['speed1'] = int(m[1])
                found.append('s1')
            else:
                f['speed2'] = int(m[1])
                found.append('s2')


        if m := re.search('alt\w*\s*(\d+)\s*k.*?alt\w*\s*(\d+)\s*k', line):
            f['altitude1'] = int(m[1])
            f['altitude2'] = int(m[2])
            found.append('s1')
            found.append('s2')
        elif m := re.search('alt\w*\s*(\d+)\s*k', line):
            if 'altitude2' in f:
                f['altitude1'] = int(m[1])
                found.append('s1')
            else:
                f['altitude2'] = int(m[1])
                found.append('s2')
        elif m := re.search('(\d+)\s*km\s*$', line):
            if 'altitude2' in f:
                f['altitude1'] = int(m[1])
                found.append('s1')
            else:
                f['altitude2'] = int(m[1])
                found.append('s2')
        elif m := re.search('(\d+)\s*km[^/][^h]', line):
            if 'altitude2' in f:
                f['altitude1'] = int(m[1])
                found.append('s1')
            else:
                f['altitude2'] = int(m[1])
                found.append('s2')

    for f in frames:
        print(f"{f.get('framenr', -1):>6d} {f.get('t', -1):>6d}   {f.get('speed1', -1):>6d}   {f.get('speed2', -1):>6d}     {f.get('altitude1', -1):>6d}   {f.get('altitude2', -1):>6d}")

if __name__=='__main__':
    main()
