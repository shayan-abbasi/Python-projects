def harmonic(n):
    total = 0.0
    for i in range(1, n + 1):
        total += 1.0 / i
    return total


try:
    
    user_input = input("")
    
    
    numbers = user_input.split()
    
    for num in numbers:
        n = int(num)
        value = harmonic(n)
        print(f"{n} {value}")

except ValueError:
    print("")