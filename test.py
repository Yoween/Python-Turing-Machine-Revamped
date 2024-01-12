import timeit
import math

# Define a sample value
x = 15

# Using x**0.5
time_x_pow = timeit.timeit(lambda: x**0.5, number=1000000)

# Using math.sqrt(x)
time_math_sqrt = timeit.timeit(lambda: math.sqrt(x), number=1000000)

print(f'Time for x**0.5: {time_x_pow}')
print(f'Time for math.sqrt(x): {time_math_sqrt}')
