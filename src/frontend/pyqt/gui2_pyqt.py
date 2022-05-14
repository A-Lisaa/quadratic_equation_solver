from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi

from ...backend.equation import Equation
from ...utils.logger import get_logger

_logger = get_logger(__file__)
app = QApplication([])
win = loadUi("./src/frontend/pyqt/2_03.ui")
equations = []
index = -1


def p():
    win.lineEdit.insert("pi")


def e():
    win.lineEdit.insert("e")


def f():
    win.lineEdit.insert("f")


def sin():
    win.lineEdit.insert("sin(")


def tg():
    win.lineEdit.insert("tg(")


def x2():
    win.lineEdit.insert("x²")


def x():
    win.lineEdit.insert("x")


def multiplu():
    win.lineEdit.insert("*")


def split():
    win.lineEdit.insert("÷")


def cos():
    win.lineEdit.insert("cos(")


def ctg():
    win.lineEdit.insert("ctg(")


def plus():
    win.lineEdit.insert("+")


def minus():
    win.lineEdit.insert("-")


def comma():
    win.lineEdit.insert(".")


def left():
    win.lineEdit.insert("(")


def sqrt():
    win.lineEdit.insert("sqrt(")


def right():
    win.lineEdit.insert(")")


def equals():
    win.lineEdit.insert("=")


def clear():
    win.lineEdit.clear()


def delete():
    win.lineEdit.backspace()


def one():
    win.lineEdit.insert("1")


def two():
    win.lineEdit.insert("2")


def three():
    win.lineEdit.insert("3")


def four():
    win.lineEdit.insert("4")


def five():
    win.lineEdit.insert("5")


def six():
    win.lineEdit.insert("6")


def seven():
    win.lineEdit.insert("7")


def eight():
    win.lineEdit.insert("8")


def nine():
    win.lineEdit.insert("9")


def zero():
    win.lineEdit.insert("0")


def y(event):
    if event.key() == Qt.Key.Key_X:
        win.x_Button.click()
    if event.key() == Qt.Key.Key_AsciiCircum:
        win.x2_Button.click()

    if event.key() == Qt.Key.Key_Up:
        win.previousButton.click()
    if event.key() == Qt.Key.Key_Backspace:
        win.deleteButton.click()
    if event.key() == Qt.Key.Key_Down:
        win.Key_Down.click()
    if event.key() == Qt.Key.Key_Return:
        win.calculateButton.click()

    if event.key() == Qt.Key.Key_Plus:
        win.plus_Button.click()
    if event.key() == Qt.Key.Key_Minus:
        win.minus_Button.click()
    if event.key() == Qt.Key.Key_Equal:
        win.equalsButton.click()
    if event.key() == Qt.Key.Key_Asterisk:
        win.multiplu_Button.click()
    if event.key() == Qt.Key.Key_Comma:
        win.comma_Button.click()
    if event.key() == Qt.Key.Key_Period:
        win.comma_Button.click()
    if event.key() == Qt.Key.Key_ParenLeft:
        win.left_Button.click()
    if event.key() == Qt.Key.Key_ParenRight:
        win.rightBracketButton.click()


    if event.key() == Qt.Key.Key_0:
        win.number0Button.click()
    if event.key() == Qt.Key.Key_1:
        win.number1Button.click()
    if event.key() == Qt.Key.Key_2:
        win.number2Button.click()
    if event.key() == Qt.Key.Key_3:
        win.number3Button.click()
    if event.key() == Qt.Key.Key_4:
        win.number4Button.click()
    if event.key() == Qt.Key.Key_5:
        win.number5Button.click()
    if event.key() == Qt.Key.Key_6:
        win.number6Button.click()
    if event.key() == Qt.Key.Key_7:
        win.number7Button.click()
    if event.key() == Qt.Key.Key_8:
        win.number8Button.click()
    if event.key() == Qt.Key.Key_9:
        win.number9Button.click()


win.keyPressEvent = y


def calc():
    global index
    try:
        equation = Equation(win.lineEdit.text())
    except Exception as e:
        _logger.critical("Exception in %s: %s", win.lineEdit.text(), e)
        win.outputField.setText(f"Выражение вызвало исключение: {e}\nНо работа продолжается")
        return
    win.outputField.setText(equation.solution)
    equations.append(equation)
    index = equations.index(equation)


def previous_equation():
    global index
    if index > 0:
        index = index - 1
        eq = equations[index]
        win.lineEdit.setText(eq.equation)
        win.outputField.setText(eq.solution)


def next_equation():
    global index
    if index < len(equations) - 1:
        index = index + 1
        eq = equations[index]
        win.lineEdit.setText(eq.equation)
        win.outputField.setText(eq.solution)


win.pi_Button.clicked.connect(p)
win.e_Button.clicked.connect(e)
win.phi_Button.clicked.connect(f)
win.sqrt_Button.clicked.connect(sqrt)
win.sin_Button.clicked.connect(sin)
win.tg_Button.clicked.connect(tg)
win.x2_Button.clicked.connect(x2)
win.cos_Button.clicked.connect(cos)
win.ctg_Button.clicked.connect(ctg)
win.x_Button.clicked.connect(x)

win.multiplu_Button.clicked.connect(multiplu)
win.split_Button.clicked.connect(split)
win.plus_Button.clicked.connect(plus)
win.minus_Button.clicked.connect(minus)
win.comma_Button.clicked.connect(comma)
win.left_Button.clicked.connect(left)
win.rightBracketButton.clicked.connect(right)
win.equalsButton.clicked.connect(equals)
win.clearButton.clicked.connect(clear)
win.deleteButton.clicked.connect(delete)
win.nextButton.clicked.connect(next_equation)
win.previousButton.clicked.connect(previous_equation)
win.calculateButton.clicked.connect(calc)


win.number1Button.clicked.connect(one)
win.number2Button.clicked.connect(two)
win.number3Button.clicked.connect(three)
win.number4Button.clicked.connect(four)
win.number5Button.clicked.connect(five)
win.number6Button.clicked.connect(six)
win.number7Button.clicked.connect(seven)
win.number8Button.clicked.connect(eight)
win.number9Button.clicked.connect(nine)
win.number0Button.clicked.connect(zero)


def main():
    win.show()
    app.exec()
