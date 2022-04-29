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


SideTerms = list[str]
Term = tuple[SideTerms, SideTerms]
Terms = tuple[Term, Term, Term]

class Equation:
    def __init__(self, equation: str):
        self.start_equation = equation
        self.normalized_equation = self.get_normalized_equation(self.start_equation)

        self._work_equation = self.normalized_equation

        self.solvability_issue = self._get_solvability_issue(self._work_equation)
        if self.solvability_issue:
            self.return_string = self.solvability_issue
            return

        self._raw_terms = self.get_raw_terms(self.normalized_equation)

        # is_one_variable = self._check_one_variable()
        # if not is_one_variable:
        #     self.return_string = "Имена переменных различны"
        #     return

        self._variable_name = self.get_variable_name()
        self._terms = self.get_terms(self._raw_terms)
        self._coefficients = self.get_coefficients(self._terms)

        self.return_string = f"{self._coefficients}"

    def _get_solvability_issue(self, equation: str) -> str:
        if not equation:
            return "Выражение пусто"

        if equation.count("=") != 1:
            return "Кол-во '=' не 1"

        splitted = equation.split("=")
        if any(map(lambda x: not x.strip(), splitted)):
            return "Хотя бы одна из сторон пуста"

        if not re.search(r"[+\-=]\s*\w*[a-zA-Z]2\s*[+\-=\s]", equation):
            return "Нет квадратного коэффициента"

        return ""

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

    def get_raw_side_terms(self, side: str) -> SideTerms:
        coefficients = re.findall(r"[+\-=][\w\(\)\*\/\+\-\.\,]+", side)
        for i, coefficient in enumerate(coefficients):
            coefficients[i] = coefficient.strip()
        return coefficients

    def get_raw_terms(self, equation: str) -> Term:
        sides = self.get_sides(equation)
        left_coefficients = self.get_raw_side_terms(sides[0])
        right_coefficients = self.get_raw_side_terms(sides[1])
        return left_coefficients, right_coefficients

    def get_side_term(
        self,
        raw_terms: SideTerms,
        pattern: str
    ) -> tuple[SideTerms, SideTerms]:
        occurrences = []
        for term in raw_terms:
            if re.search(pattern, term):
                occurrences.append(term.strip())
                raw_terms.remove(term)
        return raw_terms, occurrences

    def get_term(
        self,
        raw_terms: Term,
        pattern: str
    ) -> tuple[Term, Term]:
        left_terms, left_side = self.get_side_term(raw_terms[0], pattern)
        right_terms, right_side = self.get_side_term(raw_terms[1], pattern)
        return (left_terms, right_terms), (left_side, right_side)

    def get_terms(self, raw_terms: Term) -> Terms:
        raw_terms, quadratic_terms = self.get_term(raw_terms, r"[a-zA-Z]2$")
        raw_terms, linear_terms = self.get_term(raw_terms, r"[a-zA-Z]$")
        raw_terms, free_terms = self.get_term(raw_terms, r"$")

        if raw_terms[0] or raw_terms[1]:
            raise RuntimeError(f"Coefficients is not empty: {raw_terms}")

        return quadratic_terms, linear_terms, free_terms

    def get_coefficients(self, terms: Terms) -> Terms:
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

    def float_convertible(self, value: str) -> bool:
        try:
            float(value)
            return True
        except ValueError:
            return False

    def string_in_constants(self, value: str) -> bool:
        for constant in CONSTANTS:
            if value.endswith(constant):
                return True
        return False

    def _check_one_variable(self) -> bool:
        terms = self._raw_terms[0] + self._raw_terms[1]
        expected_variable = terms[0][-2]
        for term in terms:
            if (
                not (
                    # Заканчивается на {буква}2, aka является квадратным коэф.
                    term.endswith(f"{expected_variable}2")
                    # Заканчивается на {буква}, aka является линейным коэф.
                    or term.endswith(f"{expected_variable}")
                    or (
                        # Можно преобразовать в вещественное число
                        self.float_convertible(term)
                        # Заканчивается закрывающей скобкой (функции)
                        or term.endswith(")")
                        # Заканчивается на константу
                        or self.string_in_constants(term)
                        # Является свободным членом
                    )
                )
            ):
                return False
        return True

    def get_variable_name(self) -> str:
        terms = self._raw_terms[0] + self._raw_terms[1]
        return terms[0][-2]

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
    equation = Equation("sin(cos(tg(pi*sin(sqrt(5.5)))) = x2")
    print(equation.return_string)
    print(equation._terms)
    print(equation._coefficients)


if __name__ == "__main__":
    main()
