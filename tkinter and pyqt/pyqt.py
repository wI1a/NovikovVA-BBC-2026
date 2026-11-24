import math
import sys

from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                             QLabel, QLineEdit, QComboBox, QPushButton, QMessageBox)


class App(QWidget):
    U = ["celsius", "fahrenheit", "kelvin"]

    def __init__(self):
        super().__init__()
        self.setWindowTitle("temperature converter (pyqt)")
        self.resize(350, 250)

        v = QVBoxLayout()
        v.addWidget(QLabel("enter temperature:"))

        self.e = QLineEdit()
        self.e.returnPressed.connect(self.go)
        v.addWidget(self.e)

        h = QHBoxLayout()
        self.a = QComboBox()
        self.a.addItems(self.U)
        self.b = QComboBox()
        self.b.addItems(self.U)
        self.b.setCurrentText("fahrenheit")
        h.addWidget(self.a)
        h.addWidget(self.b)
        v.addLayout(h)

        h = QHBoxLayout()
        c = QPushButton("convert")
        c.clicked.connect(self.go)
        s = QPushButton("swap")
        s.clicked.connect(self.swap)
        h.addWidget(c)
        h.addWidget(s)
        v.addLayout(h)

        self.r = QLabel("result: ")
        self.r.setStyleSheet("font-weight: bold; font-size: 14px;")
        v.addWidget(self.r)

        self.setLayout(v)

    def to_c(self, v, u):
        if u == "fahrenheit":
            return (v - 32) * 5 / 9
        if u == "kelvin":
            return v - 273.15
        return v

    def from_c(self, v, u):
        if u == "fahrenheit":
            return v * 9 / 5 + 32
        if u == "kelvin":
            return v + 273.15
        return v

    def swap(self):
        a, b = self.a.currentText(), self.b.currentText()
        self.a.setCurrentText(b)
        self.b.setCurrentText(a)

    def go(self):
        try:
            v = float(self.e.text().replace(",", "."))
            if not math.isfinite(v):
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "input error", "enter a correct number")
            return

        c = self.to_c(v, self.a.currentText())
        if c < -273.15:
            QMessageBox.warning(self, "input error", "below absolute zero")
            return

        self.r.setText(f"result: {self.from_c(c, self.b.currentText()):.2f} {self.b.currentText()}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = App()
    w.show()
    sys.exit(app.exec())
