def FirstFactorial(num):
    n = int(num)
    result = 1
    for i in range(1, n):
        result *= i
    return result

print(FirstFactorial(input()))
