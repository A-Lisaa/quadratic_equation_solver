import re

from .parser import Parser
from .solver import Solver


def determine_sign(number: float) -> str:
    return "+" if number > 0 else "-"


def try_to_int(number: float) -> int | float:
    number_str = str(number)
    if number_str[number_str.index('.') + 1:] == '0':
        return int(number)
    else:
        return number


class Equation:
    def __init__(self, equation: str):
        self.equation = equation

        self.solvability_issue = self.get_solvability_issue(self.equation)
        if self.solvability_issue:
            self.solvable = False
            self.solution = self.solvability_issue
            return

        self.parser = Parser(self.equation)

        self.variable_name = self.parser.variable_name

        if not self.variable_name:
            self.solvable = False
            self.solution = "Имена переменных различны"
            return

        self.solver = Solver(self.parser.coefficients)

        self.a = self.solver.a
        self.b = self.solver.b
        self.c = self.solver.c

        self.discriminant = self.solver.discriminant

        self.root1 = self.solver.root1
        self.root2 = self.solver.root2

        self.solution = self.get_return_string()

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

        a_left_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[0][0])
        a_right_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[0][1])
        a = self.solver.calculate_coefficient(self.parser.coefficients[0])

        b_left_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[1][0])
        b_right_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[1][1])
        b_left_sign = determine_sign(b_left_side)
        b_right_sign = determine_sign(b_left_side)
        b = self.solver.calculate_coefficient(self.parser.coefficients[1])
        b_sign = determine_sign(b)

        c_left_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[2][0])
        c_right_side = self.solver.calculate_coefficient_same_side(self.parser.coefficients[2][1])
        c_left_sign = determine_sign(c_left_side)
        c_right_sign = determine_sign(c_right_side)
        c = self.solver.calculate_coefficient(self.parser.coefficients[2])
        c_sign = determine_sign(c)

        summed_left_side = f"{a_left_side}{self.variable_name}² {b_left_sign} {str(b_left_side).replace('-', '') if '-' in str(b_left_side) else self.b}{self.variable_name} {c_left_sign} {str(c_left_side).replace('-', '') if '-' in str(c_left_side) else c_left_side}"
        summed_right_side = f"{a_right_side}{self.variable_name}² {b_right_sign} {str(b_right_side).replace('-', '') if '-' in str(b_right_side) else b_right_side}{self.variable_name} {c_right_sign} {str(c_right_side).replace('-', '') if '-' in str(c_right_side) else c_right_side} "
        summed_equation = f"{a}{self.variable_name}² {b_sign} {str(b).replace('-', '') if '-' in str(b) else self.b}{self.variable_name} {c_sign} {str(c).replace('-', '') if '-' in str(c) else c} = 0"
        discriminant = f"D = b² - 4ac = {b ** 2}² - 4 * ({a}) * ({c}) = {self.discriminant}"

        if self.discriminant > 0:
            if a_right_side != 0 or b_right_side != 0 or c_right_side != 0:
                root1 = f"{self.variable_name}₁ = (-b + √discriminant)/(2 * a) = (-({b}) + √{self.discriminant})/(2 * {a}) = {self.root1}"
                root2 = f"{self.variable_name}₂ = (-b - √discriminant)/(2 * a) = (-({b}) - √{self.discriminant})/(2 * {a}) = {self.root2}"
                return f"""{self.equation}
{summed_left_side} = {summed_right_side}
{summed_equation}
{discriminant}
{root1}
{root2}"""
            else:
                root1 = f"{self.variable_name}₁ = (-b + √discriminant)/(2 * a) = (-({b}) + √{self.discriminant})/(2 * {a}) = {self.root1}"
                root2 = f"{self.variable_name}₂ = (-b - √discriminant)/(2 * a) = (-({b}) - √{self.discriminant})/(2 * {a}) = {self.root2}"
                return f"""{self.equation}
{summed_equation}
{discriminant}
{root1}
{root2}"""
        elif self.discriminant == 0:
            if a_right_side != 0 or b_right_side != 0 or c_right_side != 0:
                root1 = f"{self.variable_name}₁ = (-b + √discriminant)/(2 * a) = (-({b}) + √{self.discriminant})/(2 * {a}) = {self.root1}"
                return f"""{self.equation}
{summed_left_side} = {summed_right_side}
{summed_equation}
{discriminant}
{root1}"""
            else:
                root1 = f"{self.variable_name}₁ = (-b + √discriminant)/(2 * a) = (-({b}) + √{self.discriminant})/(2 * {a}) = {self.root1}"
                return f"""{self.equation}
{summed_equation}
{discriminant}
{root1}"""
