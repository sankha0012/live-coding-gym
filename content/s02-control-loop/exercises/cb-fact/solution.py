def FirstFactorial(num):
    n = int(num)          # input() gives a string
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

print(FirstFactorial(input()))
