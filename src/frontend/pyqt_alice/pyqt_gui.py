import sys

# pylint: disable=no-name-in-module, broad-except
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QMainWindow

from ...backend.equation import Equation
from ...backend.logger import get_logger
from .pyqt_mainwindow import Ui_MainWindow

_logger = get_logger(__file__)

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
        self.ui.clearButton.clicked.connect(self.clear_equation)
        self.ui.deleteButton.clicked.connect(self.delete_sign)

        self.ui.piButton.clicked.connect(lambda: self.add_equation_part("pi"))
        self.ui.eButton.clicked.connect(lambda: self.add_equation_part("e"))
        self.ui.phiButton.clicked.connect(lambda: self.add_equation_part("phi"))

        self.ui.sinButton.clicked.connect(lambda: self.add_equation_part("sin("))
        self.ui.tgButton.clicked.connect(lambda: self.add_equation_part("tg("))
        self.ui.cosButton.clicked.connect(lambda: self.add_equation_part("cos("))
        self.ui.ctgButton.clicked.connect(lambda: self.add_equation_part("ctg("))
        self.ui.sqrtButton.clicked.connect(lambda: self.add_equation_part("sqrt("))
        self.ui.lnButton.clicked.connect(lambda: self.add_equation_part("ln("))

        self.ui.number0Button.clicked.connect(lambda: self.add_equation_part("0"))
        self.ui.number1Button.clicked.connect(lambda: self.add_equation_part("1"))
        self.ui.number2Button.clicked.connect(lambda: self.add_equation_part("2"))
        self.ui.number3Button.clicked.connect(lambda: self.add_equation_part("3"))
        self.ui.number4Button.clicked.connect(lambda: self.add_equation_part("4"))
        self.ui.number5Button.clicked.connect(lambda: self.add_equation_part("5"))
        self.ui.number6Button.clicked.connect(lambda: self.add_equation_part("6"))
        self.ui.number7Button.clicked.connect(lambda: self.add_equation_part("7"))
        self.ui.number8Button.clicked.connect(lambda: self.add_equation_part("8"))
        self.ui.number9Button.clicked.connect(lambda: self.add_equation_part("9"))

        self.ui.leftBracketButton.clicked.connect(lambda: self.add_equation_part("("))
        self.ui.rightBracketButton.clicked.connect(lambda: self.add_equation_part(")"))
        self.ui.plusButton.clicked.connect(lambda: self.add_equation_part("+"))
        self.ui.minusButton.clicked.connect(lambda: self.add_equation_part("-"))
        self.ui.multiplyButton.clicked.connect(lambda: self.add_equation_part("*"))
        self.ui.equalsButton.clicked.connect(lambda: self.add_equation_part("="))
        self.ui.commaButton.clicked.connect(lambda: self.add_equation_part("."))

        self.ui.xSquaredButton.clicked.connect(lambda: self.add_equation_part("²"))
        self.ui.xButton.clicked.connect(lambda: self.add_equation_part("x"))

    def keyPressEvent(self, event):
        events = {
            Qt.Key.Key_X: self.ui.xButton.click,
            Qt.Key.Key_AsciiCircum: self.ui.xSquaredButton.click,
            Qt.Key.Key_Up: self.ui.previousButton.click,
            Qt.Key.Key_Down: self.ui.nextButton.click,
            Qt.Key.Key_PageUp: self.ui.previousButton.click,
            Qt.Key.Key_PageDown: self.ui.nextButton.click,

            Qt.Key.Key_0: self.ui.number0Button.click,
            Qt.Key.Key_1: self.ui.number1Button.click,
            Qt.Key.Key_2: self.ui.number2Button.click,
            Qt.Key.Key_3: self.ui.number3Button.click,
            Qt.Key.Key_4: self.ui.number4Button.click,
            Qt.Key.Key_5: self.ui.number5Button.click,
            Qt.Key.Key_6: self.ui.number6Button.click,
            Qt.Key.Key_7: self.ui.number7Button.click,
            Qt.Key.Key_8: self.ui.number8Button.click,
            Qt.Key.Key_9: self.ui.number9Button.click,

            Qt.Key.Key_Backspace: self.ui.deleteButton.click,
            Qt.Key.Key_Return: self.ui.calculateButton.click,

            Qt.Key.Key_Plus: self.ui.plusButton.click,
            Qt.Key.Key_Minus: self.ui.minusButton.click,
            Qt.Key.Key_Equal: self.ui.equalsButton.click,
            Qt.Key.Key_Asterisk: self.ui.multiplyButton.click,
            Qt.Key.Key_Comma: self.ui.commaButton.click,
            Qt.Key.Key_Period: self.ui.commaButton.click,
            Qt.Key.Key_ParenLeft: self.ui.leftBracketButton.click,
            Qt.Key.Key_ParenRight: self.ui.rightBracketButton.click,
        }

        events.get(event.key(), lambda: None)()

    def add_equation_part(self, part: str):
        self.ui.inputField.insert(f"{part}")

    def delete_sign(self):
        self.ui.inputField.backspace()

    def clear_equation(self):
        self.ui.inputField.clear()

    def update_equation(self):
        equation = self.equations[self.equation_index]
        self.ui.inputField.setText(equation.equation)
        self.ui.outputField.setText(equation.solution)

    def previous_equation(self):
        if self.equation_index > 0:
            self.equation_index -= 1
            self.update_equation()

    def next_equation(self):
        if self.equation_index < len(self.equations)-1:
            self.equation_index += 1
            self.update_equation()

    def calculate_equation(self):
        equation_text = self.ui.inputField.text()
        try:
            equation = Equation(equation_text)
        except Exception as e:
            _logger.critical("Exception in %s: %s", equation_text, e)
            self.ui.outputField.setText(f"Выражение вызвало исключение: {e}")
            return
        if equation not in self.equations:
            self.equations.append(equation)
        self.equation_index = self.equations.index(equation)
        self.ui.outputField.setText(equation.solution)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    try:
        app.exec()
    except Exception as e:
        _logger.critical("Exception %s", e)
