import math
from typing import Literal

from .logger import get_logger
from .parser import Parser
from .solver import Solver
from .type_aliases import AllCoefficients

_logger = get_logger(__file__)


def is_real(number: float) -> bool:
    number_str = str(float(number))
    # 15 - максимальное кол-во знаков после запятой, в иррациональном числе все 15 знаков заняты
    if len(number_str.split(".")[1]) == 15:
        return False
    return True


def determine_sign(number: float) -> Literal["+", "-"]:
    if number > 0:
        return "+"
    return "-"


def try_to_int(number: float) -> float:
    number = float(number)
    if number.is_integer():
        return int(number)
    return number


def parenthesize(number: float) -> str:
    if number < 0:
        return f"({number})"
    return str(number)


def gcd(*numbers: float) -> float:
    ten_multiplier = 10**max(len(str(float(number)).split(".")[1]) for number in numbers)
    numbers_gcd = math.gcd(*(int(number*ten_multiplier) for number in numbers))
    return numbers_gcd/ten_multiplier


class Equation:
    def __init__(self, equation: str):
        self.equation = equation

        self.solvability_issue = self.get_solvability_issue(self.equation)
        if self.solvability_issue:
            self.make_unsolvable(self.solvability_issue)
            return

        parser = Parser(self.equation)
        self.coefficients = parser.coefficients

        self.a = Solver.calculate_coefficient(self.coefficients[0])
        self.b = Solver.calculate_coefficient(self.coefficients[1])
        self.c = Solver.calculate_coefficient(self.coefficients[2])
        self.discriminant = Solver.get_discriminant(self.a, self.b, self.c)
        self.root1, self.root2 = Solver.get_roots(self.discriminant, self.a, self.b)

        _logger.info(
            "Solved %s with a = %d, b = %d, c = %d, discriminant = %d, root1 = %d, root2 = %d",
            self.equation,
            self.a,
            self.b,
            self.c,
            self.discriminant,
            self.root1,
            self.root2
        )

        self.solution = self.construct_return_string(
            self.coefficients,
            self.a,
            self.b,
            self.c,
            self.discriminant,
            self.root1,
            self.root2,
        )

    def make_unsolvable(self, reason: str):
        self.solvable = False
        self.solution = reason
        self.a = None
        self.b = None
        self.c = None
        self.discriminant = None
        self.root1 = None
        self.root2 = None
        _logger.info("%s is unsolvable: %s", self.equation, reason)

    def get_solvability_issue(self, equation: str) -> str:
        if not equation:
            return "Выражение пусто"

        if equation.count("=") != 1:
            return "Кол-во '=' не 1"

        splitted = equation.split("=")
        if any(map(lambda x: not x.strip(), splitted)):
            return "Хотя бы одна из сторон пуста"

        if not ("x²" in equation or "x*x" in equation):
            return "Нет квадратного коэффициента"

        if equation.count("(") != equation.count(")"):
            return "Кол-во открывающих и закрывающих скобок не равно"

        return ""

    def construct_return_string(
        self,
        coefficients: AllCoefficients,
        a: float,
        b: float,
        c: float,
        discriminant: float,
        root1: float | None,
        root2: float | None,
    ) -> str:
        if root1 is None and root2 is None:
            return "Нет действительных решений"

        a = try_to_int(a)
        b = try_to_int(b)
        c = try_to_int(c)
        discriminant = try_to_int(discriminant)
        discriminant_sqrt = try_to_int(discriminant**0.5)
        if root1 is not None:
            root1 = try_to_int(root1)
        if root2 is not None:
            root2 = try_to_int(root2)

        a_left_side = Solver.calculate_coefficient_same_side(coefficients[0][0])
        a_right_side = Solver.calculate_coefficient_same_side(coefficients[0][1])

        b_left_side = Solver.calculate_coefficient_same_side(coefficients[1][0])
        b_right_side = Solver.calculate_coefficient_same_side(coefficients[1][1])
        b_left_sign = determine_sign(b_left_side)
        b_right_sign = determine_sign(b_left_side)
        b_sign = determine_sign(b)

        c_left_side = Solver.calculate_coefficient_same_side(coefficients[2][0])
        c_right_side = Solver.calculate_coefficient_same_side(coefficients[2][1])
        c_left_sign = determine_sign(c_left_side)
        c_right_sign = determine_sign(c_right_side)
        c_sign = determine_sign(c)

        a_left_term = f"{a_left_side}x²"
        b_left_term = f"{b_left_sign} {str(b_left_side).replace('-', '')}x"
        c_left_term = f"{c_left_sign} {str(c_left_side).replace('-', '')}"
        summed_left_side = f"{a_left_term} {b_left_term} {c_left_term}"

        a_right_term = f"{a_right_side}x²"
        b_right_term = f"{b_right_sign} {str(b_right_side).replace('-', '')}x"
        c_right_term = f"{str(c_right_side).replace('-', '')}"
        summed_right_side = f"{a_right_term} {b_right_term} {c_right_sign} {c_right_term}"

        a_term = f"{a}x²"
        b_term = f"{b_sign} {str(b).replace('-', '')}x"
        c_term = f"{c_sign} {str(c).replace('-', '')}"
        summed_equation = f"{a_term} {b_term} {c_term} = 0"

        coefficients_gcd = gcd(a, b, c)
        if coefficients_gcd != 1.0:
            a = try_to_int(a/coefficients_gcd)
            b = try_to_int(b/coefficients_gcd)
            c = try_to_int(c/coefficients_gcd)
            discriminant = try_to_int(b*b - 4*a*c)
            a_term = f"{a}x²"
            b_term = f"{b_sign} {str(b).replace('-', '')}x"
            c_term = f"{c_sign} {str(c).replace('-', '')}"
            reduced_equation = f"{a_term} {b_term} {c_term} = 0"
        else:
            reduced_equation = ""

        discriminant_string = f"D = b² - 4*a*c = {b}² - 4*{parenthesize(a)}*{parenthesize(c)} = {b*b} - {parenthesize(4*a*c)} = {discriminant}"

        if root2 is None:
            formula = "-b/(2*a)"

            values_formula = f"-{parenthesize(b)}/(2*{parenthesize(a)})"

            final_formula = f"{-b}/{parenthesize(2*a)}"

            root1_string = f"x₁ = {formula} = {values_formula} = {final_formula} = {root1}"
            if a_right_side != 0 or b_right_side != 0 or c_right_side != 0:
                return_str = f"""
                    {summed_left_side} = {summed_right_side}
                    {summed_equation}
                    {reduced_equation}
                    {discriminant_string}
                    {root1_string}
                """
            else:
                return_str = f"""
                    {summed_equation}
                    {reduced_equation}
                    {discriminant_string}
                    {root1_string}
                """
        else:
            formula1 = "(-b + √discriminant)/(2*a)"
            formula2 = "(-b - √discriminant)/(2*a)"

            values_formula1 = f"(-{parenthesize(b)} + √{discriminant})/(2*{parenthesize(a)})"
            values_formula2 = f"(-{parenthesize(b)} - √{discriminant})/(2*{parenthesize(a)})"

            if is_real(discriminant_sqrt):
                extracted_root_formula1 = f"({-b} + {discriminant_sqrt})/{parenthesize(2*a)}"
                extracted_root_formula2 = f"({-b} - {discriminant_sqrt})/{parenthesize(2*a)}"
            else:
                extracted_root_formula1 = f"({-b} + √{discriminant})/{parenthesize(2*a)}"
                extracted_root_formula2 = f"({-b} - √{discriminant})/{parenthesize(2*a)}"

            final_formula1 = f"{-b + discriminant_sqrt}/{parenthesize(2*a)}"
            final_formula2 = f"{-b - discriminant_sqrt}/{parenthesize(2*a)}"

            root1_string = f"x₁ = {formula1} = {values_formula1} = {extracted_root_formula1} = {final_formula1} = {root1}"
            root2_string = f"x₂ = {formula2} = {values_formula2} = {extracted_root_formula2} = {final_formula2} = {root2}"

            if a_right_side != 0 or b_right_side != 0 or c_right_side != 0:
                return_str = f"""
                    {summed_left_side} = {summed_right_side}
                    {summed_equation}
                    {reduced_equation}
                    {discriminant_string}
                    {root1_string}
                    {root2_string}
                """
            else:
                return_str = f"""
                    {summed_equation}
                    {reduced_equation}
                    {discriminant_string}
                    {root1_string}
                    {root2_string}
                """

        return "\n".join(line.strip() for line in return_str.split("\n") if line.strip()).strip()
