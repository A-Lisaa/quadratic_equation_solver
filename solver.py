import math
import re


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
    occurrences = re.finditer(pattern, equation)
    coefficients = (re.search(r"[+-][+-]?(\d*\.)?\d+", occurrence[0])[0] for occurrence in occurrences)

    return sum((float(i) for i in coefficients))


def get_all_coefficients(equation: str) -> tuple[float, float, float]:
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


def get_one_root_dict(equation: str, a: float, b: float, c: float) -> dict[str, str]:
    """Создает словарь с решением ураанения, если в нем один корень
    Args:
        equation (str): уравнение, введеное пользователем
        a, b, c (str): коэф. уравнения

    Returns:
        dict[str, str]: словарь
    """
    root = -b/(2*a)

    # a_coefficient_sign = "-" if a < 0 else "+"
    b_coefficient_sign = "-" if b < 0 else "+"
    c_coefficient_sign = "-" if c < 0 else "+"

    coefficient_gcd = math.gcd(abs(int(a)), abs(int(b)), abs(int(c)))

    a_gcd = a/coefficient_gcd
    b_gcd = b/coefficient_gcd
    c_gcd = c/coefficient_gcd

    solution = {}

    solution['origin'] = equation
    solution['normalized'] = f'{a}x² {b_coefficient_sign} {abs(b)}x {c_coefficient_sign} {abs(c)} = 0'
    solution['reduced'] = f'{a_gcd}x² {b_coefficient_sign} {abs(b)/coefficient_gcd}x {c_coefficient_sign} {abs(c)/coefficient_gcd} = 0'
    solution['discriminant'] = f'D = b² - 4ac = {b_gcd}² - 4 * ({a_gcd}) * ({c_gcd}) = 0'
    solution['root'] = f'x = -b/(2a) = ({b_gcd})/({2*a_gcd}) = {root}'
    return solution


def get_two_roots_str(equation: str, a: float, b: float, c: float, discriminant: float) -> dict[str, str]:
    """Создает словарь с решением уравнения, если в нем два корня
    Args:
        equation (str): уравнение, введеное пользователем
        a, b, c (str): коэф. уравнения
        discriminant (str): дискрим. уравнения

    Returns:
        dict[str, str]: словарь
    """

    root1 = (-b + discriminant**0.5)/(2*a)
    root2 = (-b - discriminant**0.5)/(2*a)

    b_coefficient_sign = "-" if b < 0 else "+"
    c_coefficient_sign = "-" if c < 0 else "+"

    coefficient_gcd = math.gcd(abs(int(a)), abs(int(b)), abs(int(c)))

    a_gcd = a/coefficient_gcd
    b_gcd = b/coefficient_gcd
    c_gcd = c/coefficient_gcd

    solution = {}

    solution['origin'] = equation
    solution['normalized'] = f'{a}x² {b_coefficient_sign} {abs(b)}x {c_coefficient_sign} {abs(c)} = 0'
    solution['reduced'] = f'{a_gcd}x² {b_coefficient_sign} {abs(b)/coefficient_gcd}x {c_coefficient_sign} {abs(c)/coefficient_gcd} = 0'
    solution['discriminant'] = f'D = b² - 4ac = {b_gcd}² - 4 * ({a_gcd}) * ({c_gcd}) = {discriminant}'
    solution['root1'] = f'x₁ = (-b + √discriminant)/(2 * a) = (-({b_gcd}) + √{discriminant})/(2 * {a_gcd}) = {root1}'
    solution['root2'] = f'x₂ = (-b - √discriminant)/(2 * a) = (-({b_gcd}) - √{discriminant})/(2 * {a_gcd}) = {root2}'
    return solution

# √      ²      ₂       ₁


def solve_equation(equation: str) -> dict[str, str]:
    """Возвращает словарь с решением(решениями) уравнения
    Args:
        equation (str): уравнение, введеное пользователем

    Returns:
        dict[str, str]: словарь
    """
    a, b, c = get_all_coefficients(equation)
    discriminant = b*b - 4*a*c
    if discriminant > 0:
        return get_two_roots_str(equation, a, b, c, discriminant)
    elif discriminant == 0:
        return get_one_root_dict(equation, a, b, c)
    else:
        solution = {}

        solution['discriminant'] = f'D = b² - 4ac = {b}² - 4 * ({a}) * ({c}) = {discriminant} < 0'
        solution['root'] = 'Нет действительных корней'

        return solution


def input_equation() -> dict[str, str]:
    """Возвращает словарь с решением(решениями) уравнения
    Args:

    Returns:
        dict[str, str]: словарь
    """
    equation = input("Введите выражение: ")
    solution = solve_equation(equation)
    return solution


if __name__ == "__main__":
    print(input_equation())
