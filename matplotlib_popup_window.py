from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QMainWindow,
    QPushButton,
    QLabel,
    QTextEdit,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QMessageBox
)
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

class Matplotlib_Popup_Window(QMainWindow):
    def __init__(self, parent, img, title):
        super(Matplotlib_Popup_Window, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.fig = Figure()
        self.plot = self.fig.add_subplot(111)
        self.plot.axis('off')
        self.plot_widget = FigureCanvasQTAgg(figure=self.fig)
        self.plot.imshow(img)

        self.setCentralWidget(self.plot_widget)
        self.setWindowTitle(title)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def return_to_main_window(self):
        self.close()
        self.parent().show()
    
    def closeEvent(self, event):
        self.return_to_main_window()
        event.accept()