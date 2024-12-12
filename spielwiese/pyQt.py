import sys
from PyQt5.QtWidgets import QWidget, QApplication

app = QApplication(sys.argv)
w = QWidget()
w.setGeometry(100, 100, 1000, 1000)
w.setWindowTitle("myFirstGui")
w.show()
sys.exit(app.exec_())
