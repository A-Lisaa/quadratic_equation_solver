import re

from .parser import Parser
from .solver import Solver


def determine_sign(number: float) -> str:
    return "+" if number > 0 else "-"

class Equation:
    def __init__(self, equation: str):
        self.equation = equation

        parser = Parser(self.equation)

        self.solvability_issue = self.get_solvability_issue(self.equation)
        if self.solvability_issue:
            self.solvable = False
            self.return_string = self.solvability_issue
            return

        self.variable_name = parser.variable_name

        if not self.variable_name:
            self.solvable = False
            self.return_string = "Имена переменных различны"
            return

        solver = Solver(parser.coefficients)

        self.a = solver.a
        self.b = solver.b
        self.c = solver.c

        self.discriminant = solver.discriminant

        self.root1 = solver.root1
        self.root2 = solver.root2

        self.return_string = self.get_return_string()

    def get_solvability_issue(self, equation: str) -> str:
        if not equation:
            return "Выражение пусто"

        if equation.count("=") != 1:
            return "Кол-во '=' не 1"

        splitted = equation.split("=")
        if any(map(lambda x: not x.strip(), splitted)):
            return "Хотя бы одна из сторон пуста"

        if not re.search(r"[+\-=\s]*\w*[^+\-=\s]2\s*[+\-=\s]", equation):
            return "Нет квадратного коэффициента"

        return ""

    def get_return_string(self) -> str:
        if self.discriminant < 0:
            return "Нет действительных решений"

        a_sign = determine_sign(self.a)
        b_sign = determine_sign(self.b)
        c_sign = determine_sign(self.c)

        if self.discriminant > 0:
            return f"""
{self.a}{self.variable_name}² {b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self.variable_name} {c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}
x₂ = (-b - √discriminant)/(2 * a) = (-({self.b}) - √{self.discriminant})/(2 * {self.a}) = {self.root2}"""
        elif self.discriminant == 0:
            return f"""
{self.a}{self.variable_name}² {b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self.variable_name} {c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0"
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}"""

    def __str__(self):
        return self.return_string
