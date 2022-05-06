import re

from .type_aliases import (AllCoefficients, BothSidesCoefficients,
                           OneSideCoefficients)


class Parser:
    def __init__(self, equation: str):
        self.equation = self.get_normalized_equation(equation)
        self.raw_terms = self.get_raw_terms(self.equation)

        self.variable_name = self.get_variable_name(self.raw_terms)

        self.terms = self.get_terms(self.raw_terms)
        self.coefficients = self.get_coefficients(self.terms)

    def get_normalized_equation(self, equation: str) -> str:
        equation = equation.strip()
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

    def get_raw_side_terms(self, side: str) -> OneSideCoefficients:
        coefficients = re.findall(r"[+\-=][\w\s()*/\.\,]*[^+\-=]", side)
        for i, coefficient in enumerate(coefficients):
            coefficients[i] = coefficient.strip()
        return coefficients

    def get_raw_terms(self, equation: str) -> BothSidesCoefficients:
        sides = self.get_sides(equation)
        left_coefficients = self.get_raw_side_terms(sides[0])
        right_coefficients = self.get_raw_side_terms(sides[1])
        return left_coefficients, right_coefficients

    def get_variable_name(self, raw_terms: BothSidesCoefficients) -> str:
        terms = raw_terms[0] + raw_terms[1]
        expected_variable = [term for term in terms if re.search(r"\w2$", term)][0][-2]
        for term in terms:
            if re.search(r"\w[^\d]2$", term) or re.search(r"\w[^\d]$", term):
                if not re.search(rf"{expected_variable}2$", term) and not re.search(rf"{expected_variable}$", term):
                    return ""
        return expected_variable

    def get_side_term(
        self,
        raw_terms: OneSideCoefficients,
        pattern: str
    ) -> tuple[OneSideCoefficients, OneSideCoefficients]:
        occurrences = []
        for term in raw_terms:
            if re.search(pattern, term):
                occurrences.append(term.strip())
                raw_terms.remove(term)
        return raw_terms, occurrences

    def get_term(
        self,
        raw_terms: BothSidesCoefficients,
        pattern: str
    ) -> tuple[BothSidesCoefficients, BothSidesCoefficients]:
        left_terms, left_side = self.get_side_term(raw_terms[0], pattern)
        right_terms, right_side = self.get_side_term(raw_terms[1], pattern)
        return (left_terms, right_terms), (left_side, right_side)

    def get_terms(self, raw_terms: BothSidesCoefficients) -> AllCoefficients:
        raw_terms, quadratic_terms = self.get_term(raw_terms, rf"[+\-=]\s*[\w\.,()*]*{self.variable_name}2")
        raw_terms, linear_terms = self.get_term(raw_terms, rf"[+\-=]\s*[\w\.,()*]*{self.variable_name}")
        raw_terms, free_terms = self.get_term(raw_terms, r"")

        if raw_terms[0] or raw_terms[1]:
            raise RuntimeError(f"Coefficients is not empty: {raw_terms}")

        return quadratic_terms, linear_terms, free_terms

    def get_coefficients(self, terms: AllCoefficients) -> AllCoefficients:
        coefficients = (([], []), ([], []), ([], []))
        for i, term_type in enumerate(terms):
            for j, side in enumerate(term_type):
                for term in side:
                    # Убираем x2, если смотрим квадратные коэффициенты
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
