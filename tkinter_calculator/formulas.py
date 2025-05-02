import math


def calculate_factorial(window, number: str):
    try:
        num = int(number) if number else 0
        if num == 0 or num == 1:
            window.set("1")
        elif num < 0:
            window.set("Error")
        else:
            fact = 1
            for x in range(2, num + 1):
                fact *= x
            window.set(str(fact))

    except ValueError:
        window.set("Error")


def calculate_root(window, number: str):
    try:
        num = float(number) if number else 0.0
        if num < 0:
            window.set("Error")
        else:
            window.set(str(math.sqrt(num)))
    except ValueError:
        window.set("Error")
        