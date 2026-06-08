import sys
import stdio

n = int(input("How many numbers? "))

total = 0
for i in range(n):
    total += stdio.readInt()
print('Sum is %s' %total)