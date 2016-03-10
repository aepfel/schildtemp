#!/usr/bin/python

relstat = []
rel = 85
x = 128
while (x != 0):
    print rel
    print x
    if (rel >= x):
        relstat.append(True)
        rel = rel- x
    else:
        relstat.append(False)
    x = x/2

print(relstat)
