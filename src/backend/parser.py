import re

from .logger import get_logger
from .type_aliases import (AllCoefficients, RawCoefficient, RawCoefficients,
                           RawCoefficientSide, RawTerms, RawTermsSide)

_logger = get_logger(__file__)


class Parser:
    def __init__(self, equation: str):
        self.equation = self.get_normalized_equation(equation)
        self.raw_terms = self.get_raw_terms(self.equation)

        self.terms = self.get_terms(self.raw_terms)
        self.coefficients = self.get_coefficients(self.terms)

        _logger.debug("Parsed %s from %s", self.coefficients, self.equation)

    def get_normalized_equation(self, equation: str) -> str:
        equation = equation.strip()

        equation = equation.replace("x*x", "x²")

        equation = equation + "\n"

        return equation

    def get_sides(self, equation: str) -> tuple[str, str]:
        def process(part: str) -> str:
            part = part.strip()
            if not part.startswith("-"):
                part = "+" + part
            return part

        splitted = equation.split("=")

        return tuple(map(process, splitted))

    def get_raw_side_terms(self, side: str) -> RawTermsSide:
        coefficients = re.findall(r"[+\-=][\w\(\)\*\/\.\,]*[^+\-=]", side)
        for i, coefficient in enumerate(coefficients):
            coefficients[i] = coefficient.strip()
        return coefficients

    def get_raw_terms(self, equation: str) -> RawTerms:
        sides = self.get_sides(equation)
        left_coefficients = self.get_raw_side_terms(sides[0])
        right_coefficients = self.get_raw_side_terms(sides[1])
        return left_coefficients, right_coefficients

    def get_side_term(
        self, raw_terms: RawTermsSide, pattern: str
    ) -> tuple[RawTermsSide, RawCoefficientSide]:
        occurrences = []
        raw_terms_copy = raw_terms.copy()
        for term in raw_terms:
            if re.search(pattern, term):
                occurrences.append(term.strip())
                raw_terms_copy.remove(term)
        return raw_terms_copy, occurrences

    def get_term(
        self, raw_terms: RawTerms, pattern: str
    ) -> tuple[RawTerms, RawCoefficient]:
        left_terms, left_side = self.get_side_term(raw_terms[0], pattern)
        right_terms, right_side = self.get_side_term(raw_terms[1], pattern)
        return (left_terms, right_terms), (left_side, right_side)

    def get_terms(self, raw_terms: RawTerms) -> RawCoefficients:
        raw_terms, quadratic_terms = self.get_term(raw_terms, r"[+\-=][\w\.\(\)\*]*x²")
        raw_terms, linear_terms = self.get_term(raw_terms, r"[+\-=][\w\.\,\(\)\*]*x")
        raw_terms, free_terms = self.get_term(raw_terms, r"")

        if raw_terms[0] or raw_terms[1]:
            raise RuntimeError(f"Coefficients is not empty: {raw_terms}")

        return quadratic_terms, linear_terms, free_terms

    def get_coefficients(self, terms: RawCoefficients) -> AllCoefficients:
        coefficients = (([], []), ([], []), ([], []))
        for i, term_type in enumerate(terms):
            for j, side in enumerate(term_type):
                for term in side:
                    # Убираем x², если смотрим квадратные коэффициенты
                    if i == 0:
                        coefficient = term[:-2]
                    # x, если линейные
                    elif i == 1:
                        coefficient = term[:-1]
                    # ничего, если свободные члены
                    else:
                        coefficient = term

                    # Берем первый элемент коэф., это знак
                    sign = coefficient[0]
                    coefficient = coefficient.strip()

                    # Если знак составляет всю строку, то значение, надо думать, - 1
                    if sign == coefficient:
                        value = "1"
                    else:
                        value = coefficient[1:]
                        value = value.strip()

                        # Член может иметь вид: 2*x2, после убирания x2 или x может остаться *, надо убрать
                        if value.endswith("*"):
                            value = value[:-1]
                        value = value.strip()

                    coefficients[i][j].append((sign, value))
        return coefficients
