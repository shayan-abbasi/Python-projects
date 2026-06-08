import sys

total = 0
count = 0

for line in sys.stdin:
    try:
        total += float(line.strip())
        count += 1
    except ValueError:
        continue

if count > 0:
    print(f"Average: {total/count}")
