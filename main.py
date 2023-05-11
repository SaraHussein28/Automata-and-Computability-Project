from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
)
from NFA_to_DFA_GUI import NFA_To_DFA_Converter
from CFG_to_PDA_GUI import CFG_To_PDA_Converter

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        myQWidget = QWidget()
        myBoxLayout = QVBoxLayout()     

        nfaToDfa_btn = QPushButton("NFA to DFA")
        nfaToDfa_btn.clicked.connect(self.open_NFA_To_DFA_Converter)
        cfgToPda_btn = QPushButton("CFG to PDA")
        cfgToPda_btn.clicked.connect(self.open_PDA)
        myBoxLayout.addWidget(nfaToDfa_btn)     
        myBoxLayout.addWidget(cfgToPda_btn)   

        myQWidget.setLayout(myBoxLayout)
        self.setCentralWidget(myQWidget)
        self.setWindowTitle('Main Window')

    def open_NFA_To_DFA_Converter(self):
        self.hide()
        self.nfa_to_dfa_converter = NFA_To_DFA_Converter(self)
        self.nfa_to_dfa_converter.show()
        self.nfa_to_dfa_converter.center()
    
    def open_PDA(self):
        self.hide()
        self.cfg_to_pda_converter = CFG_To_PDA_Converter(self)
        self.cfg_to_pda_converter.show()
        self.cfg_to_pda_converter.center()

app = QApplication([])
mainWindow = MainWindow()
mainWindow.setFixedSize(900,500)
mainWindow.setWindowTitle('Automata Project')
mainWindow.show()
app.exec_()