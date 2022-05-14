from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi

from ...backend.equation import Equation

app = QApplication([])
win = loadUi("./src/frontend/pyqt/knopky.ui")
equations = []
index = -1


def foo(event):
    print(event.key())


win.keyPressEvent = foo

def p():
    win.lineEdit.insert("pi")
    win.lineEdit.setFocus()


def e():
    win.lineEdit.insert("e")
    win.lineEdit.setFocus()


def f():
    win.lineEdit.insert("phi")
    win.lineEdit.setFocus()


def sin():
    win.lineEdit.insert("sin()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def tg():
    win.lineEdit.insert("tg()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def sec():
    win.lineEdit.insert("sec()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arcsin():
    win.lineEdit.insert("arcsin()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arctg():
    win.lineEdit.insert("arctg()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arcsec():
    win.lineEdit.insert("arcsec()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def cos():
    win.lineEdit.insert("cos()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def ctg():
    win.lineEdit.insert("ctg()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def cosec():
    win.lineEdit.insert("cosec()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arccos():
    win.lineEdit.insert("arccos()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arcctg():
    win.lineEdit.insert("arcctg()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def arccosec():
    win.lineEdit.insert("arccosec()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def sqrt():
    win.lineEdit.insert("sqrt()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def ln():
    win.lineEdit.insert("ln()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def lg():
    win.lineEdit.insert("lg()")
    win.lineEdit.cursorBackward(False)
    win.lineEdit.setFocus()


def calc():
    global index
    equation = Equation(win.lineEdit.text())
    win.textBrowser.setText(equation.solution)
    equations.append(equation)
    index = equations.index(equation)


def back():
    global index
    if index > 0:
        index = index - 1
        eq = equations[index]
        win.lineEdit.setText(eq.equation)
        win.textBrowser.setText(eq.solution)


def forward():
    global index
    if index < len(equations) - 1:
        index = index + 1
        eq = equations[index]
        win.lineEdit.setText(eq.equation)
        win.textBrowser.setText(eq.solution)


def clear():
    win.lineEdit.clear()


win.p_button.clicked.connect(p)
win.e_button.clicked.connect(e)
win.f_button.clicked.connect(f)
win.sin_button.clicked.connect(sin)
win.tg_button.clicked.connect(tg)
win.sec_button.clicked.connect(sec)
win.arcsin_button.clicked.connect(arcsin)
win.arctg_button.clicked.connect(arctg)
win.arcsec_button.clicked.connect(arcsec)
win.cos_button.clicked.connect(cos)
win.ctg_button.clicked.connect(ctg)
win.cosec_button.clicked.connect(cosec)
win.arccos_button.clicked.connect(arccos)
win.arcctg_button.clicked.connect(arcctg)
win.arccosec_button.clicked.connect(arccosec)
win.sqrt_button.clicked.connect(sqrt)
win.ln_button.clicked.connect(ln)
win.lg_button.clicked.connect(lg)
win.calculate.clicked.connect(calc)
win.back.clicked.connect(back)
win.forward.clicked.connect(forward)
# win.clear.clicked.connect(clear)


def main():
    win.show()
    app.exec()
