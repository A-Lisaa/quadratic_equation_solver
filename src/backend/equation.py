from .parser import Parser
from .solver import Solver


def determine_sign(number: float) -> str:
    return "+" if number > 0 else "-"

class Equation:
    def __init__(self, equation: str):
        self.equation = equation

        parser = Parser(self.equation)

        self.solvability_issue = parser.get_solvability_issue()
        if self.solvability_issue:
            self.solvable = False
            self.return_string = self.solvability_issue
            return

        self._raw_terms = self.get_raw_terms(self.equation)
        self._variable_name = self.get_variable_name(self._raw_terms)
        if not self._variable_name:
            self.solvable = False
            self.return_string = "Имена переменных различны"
            return
        self._terms = self.get_terms(self._raw_terms)
        self._coefficients = self.get_coefficients(self._terms)

        solver = Solver(self._coefficients)

        self.a = solver.a
        self.b = solver.b
        self.c = solver.c

        self.discriminant = solver.discriminant

        self.root1 = solver.root1
        self.root2 = solver.root2

        self.return_string = self.get_return_string()

    def get_return_string(self) -> str:
        if self.discriminant < 0:
            return "Нет действительных решений"

        a_sign = determine_sign(self.a)
        b_sign = determine_sign(self.b)
        c_sign = determine_sign(self.c)

        if self.discriminant > 0:
            return f"""
{self.a}{self._variable_name}² {b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self._variable_name} {c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}
x₂ = (-b - √discriminant)/(2 * a) = (-({self.b}) - √{self.discriminant})/(2 * {self.a}) = {self.root2}"""
        elif self.discriminant == 0:
            return f"""
{self.a}{self._variable_name}² {b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self._variable_name} {c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0"
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}"""

    def __str__(self):
        return self.return_string
