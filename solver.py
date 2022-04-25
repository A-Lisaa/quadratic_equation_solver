import math
import re

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
    'fi': 1.6180339887
}


SideTermCoefficients = list[str]
TermCoefficients = tuple[SideTermCoefficients, SideTermCoefficients]
Coefficients = tuple[TermCoefficients, TermCoefficients, TermCoefficients]

RawSideTerms = list[str]
RawTerms = tuple[RawSideTerms, RawSideTerms]
Terms = tuple[TermCoefficients, TermCoefficients, TermCoefficients]

class Equation:
    def __init__(self, equation: str):
        self.start_equation = equation
        self.normalized_equation = self.get_normalized_equation(self.start_equation)

        self._work_equation = self.normalized_equation
        if not self.normalized_equation:
            self.return_string = "Ты че дурак, бля? Какая пустая строка, нахуй?"
            return
        self._raw_terms = self.get_raw_terms(self.normalized_equation)
        self.variable_name = self.get_variable_name()
        self._terms = self.get_terms(self._raw_terms)
        self._coefficients = self.get_coefficients(self._terms)

        self.return_string = f"{self._terms}; {self._coefficients}"

    def get_normalized_equation(self, equation: str) -> str:
        equation = equation.strip()

        return equation

    def get_sides(self, equation: str) -> tuple[str, str]:
        def process(part: str) -> str:
            part = part.strip()
            if not part.startswith("-"):
                part = "+" + part
            return part

        splitted = equation.split("=")

        return tuple(map(process, splitted))

    def get_raw_side_terms(self, side: str) -> RawSideTerms:
        coefficients = re.findall(r"[+\-=][^+\-=]*", side)
        for i, coefficient in enumerate(coefficients):
            coefficients[i] = coefficient.strip()
        return coefficients

    def get_raw_terms(self, equation: str) -> RawTerms:
        sides = self.get_sides(equation)
        left_coefficients = self.get_raw_side_terms(sides[0])
        right_coefficients = self.get_raw_side_terms(sides[1])
        return left_coefficients, right_coefficients

    def get_side_term(
        self,
        raw_terms: RawSideTerms,
        pattern: str
    ) -> tuple[RawSideTerms, SideTermCoefficients]:
        occurrences = []
        for term in raw_terms:
            if re.search(pattern, term):
                occurrences.append(term.strip())
                raw_terms.remove(term)
        return raw_terms, occurrences

    def get_term(
        self,
        raw_terms: RawTerms,
        pattern: str
    ) -> tuple[RawTerms, TermCoefficients]:
        left_terms, left_side = self.get_side_term(raw_terms[0], pattern)
        right_terms, right_side = self.get_side_term(raw_terms[1], pattern)
        return (left_terms, right_terms), (left_side, right_side)

    def get_terms(self, raw_terms: RawTerms) -> Terms:
        raw_terms, quadratic_terms = self.get_term(raw_terms, rf"{self.variable_name}2")
        raw_terms, linear_terms = self.get_term(raw_terms, rf"{self.variable_name}")
        raw_terms, free_terms = self.get_term(raw_terms, r"")

        if raw_terms[0] or raw_terms[1]:
            raise RuntimeError(f"Coefficients is not empty: {raw_terms}")

        return quadratic_terms, linear_terms, free_terms

    def get_coefficients(self, terms: Terms) -> Coefficients:
        coefficients = (([], []), ([], []), ([], []))
        for i, term_type in enumerate(terms):
            for j, side in enumerate(term_type):
                for term in side:
                    if i == 0:
                        term = term[:-2]
                    elif i == 1:
                        term = term[:-1]
                    term = term.strip()
                    while term.endswith("*"):
                        term = term[:-1]
                    term = term.strip()
                    coefficients[i][j].append(term)
        return coefficients

    def get_variable_name(self):
        terms = self._raw_terms[0] + self._raw_terms[1]
        expected_variable = terms[0][-2]
        for term in terms:
            if (
                not (
                    term.endswith(f"{expected_variable}2")
                    or term.endswith(f"{expected_variable}")
                    or term[-1].isdigit()
                )
            ):
                raise RuntimeError("Variable names differ")
        return expected_variable

    def get_discriminant(self, a: float, b: float, c: float) -> float:
        return b*b - 4*a*c

    def calculate_coefficient(self, coefficients: list[str]) -> float:
        coefficient_overall = 0
        for coefficient in coefficients:
            sign = coefficient[0]
            if '(' in coefficient:
                function = coefficient[1:coefficient.index('(')]
                argument = coefficient[coefficient.index('(') + 1:coefficient.index(')')]

                if '-' in argument:
                    if argument in CONSTANTS:
                        argument = -(CONSTANTS[argument[1:]])
                    else:
                        argument = CONSTANTS[argument]

                value = FUNCTIONS[function](float(argument))
            else:
                value = coefficient[1:]

                if value in CONSTANTS:
                    value = CONSTANTS[value]

                value = float(value)

            coefficient_overall += value if sign == "+" else -value

        return coefficient_overall


def main():
    equation = Equation("sqrt(2)*x2 + 4x -10 = -4x2")
    print(equation._terms)
    print(equation._coefficients)


if __name__ == "__main__":
    main()
