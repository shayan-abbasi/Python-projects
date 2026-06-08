def harmonic(n, r=1):
    total = 0.0
    for i in range(1, n + 1):
        total += 1.0 / (i ** r)
    return total


try:
    print("")
    n_input = int(input(""))
    r_input = input("")

   
    if r_input.strip() == "":
       
        result = harmonic(n_input)
        print(f"\n{n_input} ")
    else:
       
        r_val = int(r_input)
        result = harmonic(n_input, r=r_val)
        print(f"\n{n_input} {r_val}:")

    print(f"{result}")

except ValueError:
    print("")