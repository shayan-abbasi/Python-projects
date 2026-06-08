import sys

def harmonic(n):
    total = 0.0
    for i in range(1, n + 1):
        total += 1.0 / i
    return total


try:
    user_data = input("")
  
    args = user_data.split()
    
    for arg_str in args:
        n = int(arg_str)
        value = harmonic(n)
    
        print(value)

except ValueError:
    print("")
