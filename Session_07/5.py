import sys

def cube(i):
    j = i * i * i
    return j

if len(sys.argv) > 1:
  
    n = int(sys.argv[1])
else:

    n = 6

for i in range(1, n + 1):
    print('%s %s' % (i, cube(i)))
