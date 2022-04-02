import re
from typing import Any, Callable, Dict, List, Tuple


def normalize_equation(equation: str) -> str:
    """Normalizes equation so other methods will be able work with it
    Args:
        equation (str): equation to normailze
    Returns:
        str: normalized equation
    """
    # We remove whitespaces to not have problems
    # But we add a whitespace to the end so we can detect the end of an equation
    equation = equation.strip().replace(" ", "") + " "
    # We remove * and ^ and replace , with . just so we will have something like x2 - 3.14x + 14 = 0, not x^2 - 3,14*x + 14 = 0 and it will be easier for us to use
    equation = equation.replace("*", "").replace("^", "").replace(",", ".")
    # We add + to the beginning if there is no mark, so later we can easily check only if there is a - or +
    if not equation.startswith(("+", "-")):
        equation = "+" + equation
    # We change a variable name to x, so we don't have to fuck with different names
    equation = "".join(("x" if character.isalpha() else character for character in equation))
    # We add coefficient +-1 to anything with x if there is no coefficient, so every x will have its own coefficient
    equation = re.sub(r"\+x", "+1x", equation)
    equation = re.sub(r"\-x", "-1x", equation)

    return equation


def get_coefficient(pattern: str, equation: str) -> float:
    """Gets one and only one coefficient of an equation w/o [=] (for example: gets coefficient of a)
    Args:
        pattern (str): pattern of a coefficient to get
        equation (str): equation with coefficients
    Returns:
        Decimal: sum of all coeficients in equation
    """
    occurences = re.finditer(pattern, equation)
    coefficients = (re.search(r"[+-][+-]?(\d*\.)?\d+", occurence[0])[0] for occurence in occurences)

    return sum((float(i) for i in coefficients))


def get_all_coefficients(equation: str) -> Tuple[float, float, float]:
    """Gets all coefficients of equation w/o [=]
    Args:
        equation (str): equation from which coefficients are to be taken
    Returns:
        tuple[Decimal, Decimal, Decimal]: tuple containing (a, b, c) coefficients
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
    x1 = (-b + discriminant**0.5)/2*a
    x2 = (-b - discriminant**0.5)/2*a
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


def menu(prompt: str, actions: Dict[str, Tuple[Callable[..., Any], List[Any], Dict[str, Any]]], start_number: int = 1):
    actions = {str(k): v for k, v in enumerate(actions.values(), start=start_number)}
    while True:
        print(prompt)
        print("Выберите вариант ответа из предложенных: ", end="")
        for position, action in enumerate(actions, start=start_number):
            print(f"{position}) {action}")
        answer = input()
        if answer in actions:
            break
        print("Неверный вариант")

    actions[answer][0](*actions[answer][1], **actions[answer][2])

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
