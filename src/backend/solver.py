import math

from .type_aliases import (AllCoefficients, BothSidesCoefficients,
                           OneSideCoefficients, Roots)

FUNCTIONS = {
    'sqrt': math.sqrt,
    'ln': math.log,

    'sin': math.sin,
    'tg': math.tan,
    'sec': lambda x: 1/math.cos(x),

    'cos': math.cos,
    'ctg': lambda x: 1/math.tan(x),
    'cosec': lambda x: 1/math.sin(x),
}


CONSTANTS = {
    'pi': math.pi,
    'e': math.e,
    'phi': 1.6180339887
}


class Solver:
    def __init__(self, coefficients: AllCoefficients):
        self.coefficients = coefficients

        self.a = self.calculate_coefficient(self.coefficients[0])
        self.b = self.calculate_coefficient(self.coefficients[1])
        self.c = self.calculate_coefficient(self.coefficients[2])

        self.discriminant = self.get_discriminant(self.a, self.b, self.c)

        self.root1, self.root2 = self.get_roots(self.a, self.b, self.discriminant)

    def get_discriminant(self, a: float, b: float, c: float) -> float:
        return b*b - 4*a*c

    def calculate_coefficient_same_side(self, coefficients: OneSideCoefficients) -> float:
        coefficient_sum = 0
        for coefficient in coefficients:
            sign = coefficient[0]
            value = coefficient[1]

            if '(' in value:
                function = value[:value.index('(')]
                argument = value[value.index('(')+1:value.index(')')]

                if '-' in argument:
                    if argument in CONSTANTS:
                        argument = -(CONSTANTS[argument[1:]])
                    else:
                        argument = CONSTANTS[argument]

                value = FUNCTIONS[function](float(argument))
            else:
                if value in CONSTANTS:
                    value = CONSTANTS[value]
                else:
                    value = float(value.replace(',', '.'))

            coefficient_sum += value if sign == "+" else -value
        return coefficient_sum

    def calculate_coefficient(self, coefficients: BothSidesCoefficients) -> float:
        coefficient_left = self.calculate_coefficient_same_side(coefficients[0])
        coefficient_right = self.calculate_coefficient_same_side(coefficients[1])
        return coefficient_left - coefficient_right

    def get_roots(self, discriminant: float, a: float, b: float) -> Roots:
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
