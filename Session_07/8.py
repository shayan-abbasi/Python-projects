import math

def pdf(x, mu=0.0, sigma=1.0):

    divisor = sigma * math.sqrt(2 * math.pi)
    exponent = -((x - mu)**2) / (2 * sigma**2)
    return math.exp(exponent) / divisor

mu_sat = 1019
sigma_sat = 209

print(pdf(820, mu_sat, sigma_sat))