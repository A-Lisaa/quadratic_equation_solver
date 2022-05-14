import math

from ..utils.logger import get_logger
from .type_aliases import BothSidesCoefficients, OneSideCoefficients, Roots

_logger = get_logger(__file__)

FUNCTIONS = {
    'sqrt': math.sqrt,
    'ln': math.log,

    'sin': math.sin,
    'tg': math.tan,

    'cos': math.cos,
    'ctg': lambda x: 1/math.tan(x),
}


CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'phi': 1.6180339887
}


class Solver:
    @staticmethod
    def get_discriminant(a: float, b: float, c: float) -> float:
        return b*b - 4*a*c

    @staticmethod
    def calculate_coefficient_same_side(coefficients: OneSideCoefficients) -> float:
        coefficient_sum = 0
        for coefficient in coefficients:
            sign = coefficient[0]
            value = coefficient[1]

            if '(' in value:
                function = value[:value.index('(')]
                argument = value[value.index('(')+1:value.index(')')]

                if argument in CONSTANTS:
                    if argument.startswith("-"):
                        argument = -CONSTANTS[argument]
                    else:
                        argument = CONSTANTS[argument]
                else:
                    argument = float(argument)

                value = FUNCTIONS[function](argument)
            else:
                if value in CONSTANTS:
                    value = CONSTANTS[value]
                else:
                    value = float(value.replace(',', '.'))

            coefficient_sum += value if sign == "+" else -value

        _logger.debug("Calculated sum of %s as %s", coefficients, coefficient_sum)
        return coefficient_sum

    @staticmethod
    def calculate_coefficient(coefficients: BothSidesCoefficients) -> float:
        coefficient_left = Solver.calculate_coefficient_same_side(coefficients[0])
        coefficient_right = Solver.calculate_coefficient_same_side(coefficients[1])
        return coefficient_left - coefficient_right

    @staticmethod
    def get_roots(discriminant: float, a: float, b: float) -> Roots:
        if discriminant > 0:
            root1 = (-b + discriminant**0.5)/(2*a)
            root2 = (-b - discriminant**0.5)/(2*a)
        elif discriminant == 0:
            root1 = (-b)/(2*a)
            root2 = None
        else:
            root1 = None
            root2 = None
        return root1, root2
