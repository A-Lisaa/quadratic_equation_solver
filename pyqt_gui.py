import sys

from PyQt6 import QtWidgets, uic

app = QtWidgets.QApplication(sys.argv)

window = uic.loadUi("untitled.ui")
window.textBrowser.setText("Lol kek azaza")

window.show()

app.exec()
