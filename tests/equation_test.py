import unittest

from src.backend.equation import Equation


class EquationTest(unittest.TestCase):
    def test_solvability(self):
        with open("./tests/equations.txt", encoding='utf-8') as file:
            for line in file:
                equation, answer = line.split("; ")
                answer = answer.split(" ")
                equation = equation.replace("x2", "x²")
                equation = equation.replace(" ", "")
                eq = Equation(equation)
                if answer[0] == "No_R":
                    self.assertIsNone(eq.root1)
                    self.assertIsNone(eq.root2)
                elif len(answer) == 1:
                    if eq.root1 is not None:
                        self.assertEqual(round(eq.root1, 2), float(answer[0].strip()))
                    self.assertIsNone(eq.root2)
                else:
                    if eq.root1 is not None and eq.root2 is not None:
                        roots = sorted([round(eq.root1, 2), round(eq.root2, 2)])
                        answer = sorted([round(float(answer[0].strip()), 2), round(float(answer[1].strip()), 2)])
                        self.assertEqual(roots[0], answer[0])
                        self.assertEqual(roots[1], answer[1])
