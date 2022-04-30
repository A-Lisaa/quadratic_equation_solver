from PyQt6.QtWidgets import QApplication
from PyQt6.uic import loadUi

from solver import Equation

app = QApplication([])
win = loadUi("knopky.ui")
equations = []
index = -1


def p():
    win.lineEdit.insert('pi')


def e():
    win.lineEdit.insert('e')


def f():
    win.lineEdit.insert('f')


def sin():
    win.lineEdit.insert('sin')


def tg():
    win.lineEdit.insert('tg')


def sec():
    win.lineEdit.insert('sec')


def arcsin():
    win.lineEdit.insert('arcsin')


def arctg():
    win.lineEdit.insert('arctg')


def arcsec():
    win.lineEdit.insert('arcsec')


def cos():
    win.lineEdit.insert('cos')


def ctg():
    win.lineEdit.insert('ctg')


def cosec():
    win.lineEdit.insert('cosec')


def arccos():
    win.lineEdit.insert('arccos')


def arcctg():
    win.lineEdit.insert('arcctg')


def arccosec():
    win.lineEdit.insert('arccosec')


def sqrt():
    win.lineEdit.insert('sqrt')


def ln():
    win.lineEdit.insert('ln')


def lg():
    win.lineEdit.insert('lg')


def kalc():
    global index
    equation = Equation(win.lineEdit.text())
    win.textBrowser.setText(equation)
    equations.append(equation)
    index = equations.index(equation)


def back():
    global index
    if index != 0:
        win.lineEdit.setText(equations[index])
    else:
        index = index-1
    win.lineEdit.setText(equations[index])


def forward():
    global index
    if index >= len(equations) -1:
        win.lineEdit.setText(equations[index])
    else:
        index = index+1
    win.lineEdit.setText(equations[index])


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
win.kalc.clicked.connect(kalc)
win.back.clicked.connect(back)
win.forward.clicked.connect(forward)

win.show()
app.exec()
