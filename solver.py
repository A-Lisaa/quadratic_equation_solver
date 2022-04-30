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
            self.solvable = False
            self.return_string = self.solvability_issue
            return

        self._raw_terms = self.get_raw_terms(self.normalized_equation)
        self._variable_name = self.get_variable_name(self._raw_terms)
        if not self._variable_name:
            self.solvable = False
            self.return_string = "Имена переменных различны"
            return
        self._terms = self.get_terms(self._raw_terms)
        self._coefficients = self.get_coefficients(self._terms)

        self.a = self.calculate_coefficient(self._coefficients[0])

        self.b = self.calculate_coefficient(self._coefficients[1])
        self.b_sign = '-' if self.b < 0 else '+'

        self.c = self.calculate_coefficient(self._coefficients[2])
        self.c_sign = '-' if self.c < 0 else '+'

        self.discriminant = self.get_discriminant(self.a, self.b, self.c)
        self.root1, self.root2 = self.get_roots(self.discriminant, self.a, self.b)

        if self.discriminant > 0:
            self.return_string = f"""{self.a}{self._variable_name}² {self.b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self._variable_name} {self.c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}
x₂ = (-b - √discriminant)/(2 * a) = (-({self.b}) - √{self.discriminant})/(2 * {self.a}) = {self.root2}"""
        elif self.discriminant == 0:
            self.return_string = f"""{self.a}{self._variable_name}² {self.b_sign} {str(self.b).replace('-', '') if '-' in str(self.b) else self.b}{self._variable_name} {self.c_sign} {str(self.c).replace('-', '') if '-' in str(self.c) else self.c} = 0"
D = b² - 4ac = {self.b**2}² - 4 * ({self.a}) * ({self.c}) = {self.discriminant}
x₁ = (-b + √discriminant)/(2 * a) = (-({self.b}) + √{self.discriminant})/(2 * {self.a}) = {self.root1}"""
        else:
            self.return_string = "Нет действительных решений"

    def __str__(self):
        return self.return_string

    def _get_solvability_issue(self, equation: str) -> str:
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
        coefficients = re.findall(r"[+\-=][\w\s()*/\.\,]*[^+\-=]", side)
        for i, coefficient in enumerate(coefficients):
            coefficients[i] = coefficient.strip()
        return coefficients

    def get_raw_terms(self, equation: str) -> Term:
        sides = self.get_sides(equation)
        left_coefficients = self.get_raw_side_terms(sides[0])
        right_coefficients = self.get_raw_side_terms(sides[1])
        return left_coefficients, right_coefficients

    def get_variable_name(self, raw_terms: tuple[list[str], list[str]]) -> str:
        terms = raw_terms[0] + raw_terms[1]
        expected_variable = [term for term in terms if re.search(r"\w2$", term)][0][-2]
        for term in terms:
            if re.search(r"\w[^\d]2$", term) or re.search(r"\w[^\d]$", term):
                if not re.search(rf"{expected_variable}2$", term) and not re.search(rf"{expected_variable}$", term):
                    return ""
        return expected_variable

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
        raw_terms, quadratic_terms = self.get_term(raw_terms, rf"[+\-=]\s*[\w\.,()*]*{self._variable_name}2")
        raw_terms, linear_terms = self.get_term(raw_terms, rf"[+\-=]\s*[\w\.,()*]*{self._variable_name}")
        raw_terms, free_terms = self.get_term(raw_terms, r"")

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

    def get_discriminant(self, a: float, b: float, c: float) -> float:
        return b*b - 4*a*c

    def calculate_coefficient_same_side(self, coefficient: list[tuple[str, str]]) -> float:
        coefficient_overall = 0
        for elements in coefficient:
            sign = elements[0]
            value = elements[1]

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

            coefficient_overall += value if sign == "+" else -value
        return coefficient_overall

    def calculate_coefficient(self, coefficients: tuple[list, list]) -> float:
        coefficient_left  = self.calculate_coefficient_same_side(coefficients[0])
        coefficient_right  = self.calculate_coefficient_same_side(coefficients[1])
        return coefficient_left - coefficient_right

    def get_roots(self, discriminant: float, a: float, b: float):
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


def main():
    with open('equations.txt', encoding='UTF-8') as file:
        for line in file:
            eq = line.split("; ")
            equation = Equation(eq[0])
            answer = eq[1].split(" ")
            print(equation)
            print(*answer)


if __name__ == "__main__":
    main()
