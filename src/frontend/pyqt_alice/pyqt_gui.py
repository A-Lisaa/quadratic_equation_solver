import sys

# pylint: disable=no-name-in-module
from PyQt6.QtWidgets import QApplication, QMainWindow

from ...backend.equation import Equation
from .pyqt_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.equations: list[Equation] = []
        self.equation_index = -1
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.calculateButton.clicked.connect(self.calculate_equation)
        self.ui.previousButton.clicked.connect(self.previous_equation)
        self.ui.nextButton.clicked.connect(self.next_equation)

        self.ui.piButton.clicked.connect(lambda: self.add_equation_part("pi"))
        self.ui.eButton.clicked.connect(lambda: self.add_equation_part("e"))
        self.ui.phiButton.clicked.connect(lambda: self.add_equation_part("phi"))

        self.ui.sinButton.clicked.connect(lambda: self.add_equation_part("sin()"))
        self.ui.tgButton.clicked.connect(lambda: self.add_equation_part("tg()"))
        self.ui.secButton.clicked.connect(lambda: self.add_equation_part("sec()"))

        self.ui.cosButton.clicked.connect(lambda: self.add_equation_part("cos()"))
        self.ui.ctgButton.clicked.connect(lambda: self.add_equation_part("ctg()"))
        self.ui.cosecButton.clicked.connect(lambda: self.add_equation_part("cosec()"))

        self.ui.sqrtButton.clicked.connect(lambda: self.add_equation_part("sqrt()"))
        self.ui.lnButton.clicked.connect(lambda: self.add_equation_part("ln()"))
        self.ui.emptyButton.clicked.connect(lambda: self.add_equation_part("sqrt()")) # Placeholder

    def add_equation_part(self, part: str): # sin(cos(tg(pi*sin(sqrt(5)))) = x2
        self.ui.inputField.insert(f"{part}")
        if part.endswith("()"):
            self.ui.inputField.cursorBackward(False)
        self.ui.inputField.setFocus()

    def previous_equation(self):
        if self.equation_index > 0:
            self.equation_index -= 1
        equation = self.equations[self.equation_index]
        self.ui.inputField.setText(equation.equation)
        self.ui.outputField.setText(equation.solution)

    def next_equation(self):
        if self.equation_index < len(self.equations)-1:
            self.equation_index += 1
        equation = self.equations[self.equation_index]
        self.ui.inputField.setText(equation.equation)
        self.ui.outputField.setText(equation.solution)

    def calculate_equation(self):
        equation_text = self.ui.inputField.text()
        equation = Equation(equation_text)
        if equation not in self.equations:
            self.equations.append(equation)
        self.equation_index = self.equations.index(equation)
        self.ui.outputField.setText(equation.solution)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
