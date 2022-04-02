import re
from typing import Tuple


def normalize_equation(equation: str) -> str:
    """Нормализует выражение к стандарту, чтобы все функции работали с одним видом

    Args:
        equation (str): выражение для нормализации

    Returns:
        str: нормализованное выражение
    """
    # Удаляем пробелы, чтобы не иметь проблем из-за них
    # Но нужно добавить 1 пробел в конец, чтобы определить конец выражения
    # (возможно стоит заменить на \n, например)
    equation = equation.strip().replace(" ", "") + " "
    # Удаляем * и ^ и заменяем , на . чтобы иметь одинаковый вид всех уравнений
    equation = equation.replace("*", "").replace("^", "").replace(",", ".")
    # Добавляем + к первому коэффициенту, чтобы все коэф. имели знак
    if not equation.startswith(("+", "-")):
        equation = "+" + equation
    # Меняем имя переменной на x, чтобы оно всегда было одинаковое
    equation = "".join(("x" if character.isalpha() else character for character in equation))
    # Добавляем коэффициенты +-1, если коэф. нет, чтобы везде были коэф.
    equation = re.sub(r"\+x", "+1x", equation)
    equation = re.sub(r"\-x", "-1x", equation)

    return equation


def get_coefficient(pattern: str, equation: str) -> float:
    """Получает один из коэф. выражения по паттерну

    Args:
        pattern (str): паттерн коэффициента, по которому его искать
        equation (str): выражение, из которого взять коэф.

    Returns:
        float: коэффициент
    """
    occurences = re.finditer(pattern, equation)
    coefficients = (re.search(r"[+-][+-]?(\d*\.)?\d+", occurence[0])[0] for occurence in occurences)

    return sum((float(i) for i in coefficients))


def get_all_coefficients(equation: str) -> Tuple[float, float, float]:
    """Получает все коэф. выражения

    Args:
        equation (str): выражение, из которого взять коэф.

    Returns:
        tuple[float, float, float]: кортеж (неизменяемый список) с коэф. (a, b, c)
    """
    equation = normalize_equation(equation)

    a_coefficient = get_coefficient(r"[+-][+-]?(\d*\.)?\d+x2[ =+-]", equation)
    b_coefficient = get_coefficient(r"[+-][+-]?(\d*\.)?\d+x[ =+-]", equation)
    c_coefficient = get_coefficient(r"[+-][+-]?(\d*\.)?\d+[ =+-]", equation)

    return (a_coefficient, b_coefficient, c_coefficient)


def get_one_root(a, b, discriminant):
    x = -b/(2*a)
    return f'{x}; {discriminant}'


def get_two_roots(a, b, discriminant):
    x1 = (-b + discriminant**0.5)/(2*a)
    x2 = (-b - discriminant**0.5)/(2*a)
    return f'{x1}; {x2};  {discriminant}'


def solve_equation(equation):
    a, b, c = get_all_coefficients(equation)
    discriminant = b*b - 4*a*c
    if discriminant > 0:
        return get_two_roots(a, b, discriminant)
    elif discriminant == 0:
        return get_one_root(a, b, discriminant)
    else:
        return 'Нет действительных корней'


def print_solution(equation):
    x = solve_equation(equation)
    print(x)


def get_equation():
    return input("Введите выражение: ")


def file_test():
    with open("equations.txt", encoding="utf-8") as file:
        for line in file:
            equation = line.split("; ")
            answer = equation[1].split(" ")
            print_solution(equation[0])
            print(*answer)


def input_test():
    equation = get_equation()
    print_solution(equation)


if __name__ == "__main__":
    file_test()
