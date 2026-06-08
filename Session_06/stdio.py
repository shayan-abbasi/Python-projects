import sys

# این بخش برای خواندن اعداد از ورودی به همان شکلی است که در جزوه دیدی
_buffer = []

def _read():
    global _buffer
    while not _buffer:
        line = sys.stdin.readline()
        if not line:
            return None
        _buffer = line.split()
    return _buffer.pop(0)

def readInt():
    s = _read()
    if s is None:
        return None
    return int(s)

def readFloat():
    s = _read()
    if s is None:
        return None
    return float(s)

def write(s):
    sys.stdout.write(str(s))
    sys.stdout.flush()

def writeln(s=''):
    sys.stdout.write(str(s) + '\n')
    sys.stdout.flush()