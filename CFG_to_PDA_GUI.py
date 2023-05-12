import Utils.constants as constant
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
)
import graphviz
import io
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import IO as Grammar
from cfg_to_gnf import convertToGNF
from gnf_to_pda import convert_to_PDA
from matplotlib_popup_window import Matplotlib_Popup_Window

class CFG_To_PDA_Converter(QMainWindow):
    def __init__(self, parent):
        super(CFG_To_PDA_Converter, self).__init__(parent)
        # ensure this window gets garbage-collected when closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        main_widget = QWidget()
        
        self.fig = Figure()
        self.plot = self.fig.add_subplot(111)

        self.plot_widget = FigureCanvasQTAgg(figure=self.fig)


        # input grammar subgrid

        self.input_label = QLabel('Enter CFG below. \n1. Terminals and non terminals \ncan only have a length of 1'+
                                  '\n2. Start symbol MUST be S'+
                                  '\n3. Productions MUST be in format S->ab')
        self.epsilon_button = QPushButton('Insert epsilon')
        self.epsilon_button.clicked.connect(self.insertEpsilon)

        self.grammar_input = QTextEdit()
        self.grammar_input.setTabStopWidth(15)

        
        self.input_grammar_subgrid = QVBoxLayout()

        self.input_grammar_subgrid.addWidget(self.input_label)
        self.input_grammar_subgrid.addWidget(self.epsilon_button)
        self.input_grammar_subgrid.addWidget(self.grammar_input)


        #gnf grammar subgrid
        self.gnf_grammar = QTextEdit()
        self.gnf_grammar.setTabStopWidth(15)
        self.gnf_grammar.setReadOnly(True)
        
        self.gnf_label = QLabel('GNF Grammar')

        self.gnf_grammar_subgrid = QVBoxLayout()


        self.gnf_grammar_subgrid.addWidget(self.gnf_label)
        self.gnf_grammar_subgrid.addWidget(self.gnf_grammar)


        #pda grammar subgrid
        self.pda_grammar_subgrid = QVBoxLayout()

        self.pda_grammar = QTextEdit()
        self.pda_grammar.setTabStopWidth(15)
        self.pda_grammar.setReadOnly(True)

        self.pda_label = QLabel('PDA grammar')

        self.pda_grammar_subgrid.addWidget(self.pda_label)
        self.pda_grammar_subgrid.addWidget(self.pda_grammar)


        # adding all grammar layouts in one horizontal layout
        self.grammars = QHBoxLayout()
        self.grammars.addLayout(self.input_grammar_subgrid)
        self.grammars.addLayout(self.gnf_grammar_subgrid)
        self.grammars.addLayout(self.pda_grammar_subgrid)


        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)



        grid = QVBoxLayout()


        grid.addLayout(self.grammars)
        grid.addWidget(self.submit_button)



        main_widget.setFixedSize(900, 500)
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('CFG to PDA converter')
    
    def insertEpsilon(self):
        cursor = self.grammar_input.textCursor()
        cursor.insertText(constant.EPSILON)

    def show_pda(self, res):
        self.pda_grammar.setPlainText(res)
        
    def show_gnf(self, gnf):
        self.gnf_grammar.setPlainText(gnf)

    def submit(self):
        G = graphviz.Digraph('finite_state_machine', comment='The Round Table')
        G.attr(rankdir='LR')
        input = self.grammar_input.toPlainText()
        grammar = Grammar.parse_input_grammar(input)
    
        gnf = convertToGNF(grammar)
        
        print (gnf)
        transitions = convert_to_PDA(gnf)
        pda_res = Grammar.build_PDA_output(transitions)
        print (pda_res)
        self.show_pda(pda_res)

        gnf_res = Grammar.build_gnf_grammar_output(gnf)
        self.show_gnf(gnf_res)
        graph, graph_list = Grammar.build_graph_output(G = G, transitions=transitions)
        png_bytes = graph.pipe(format='png')
        img = plt.imread(io.BytesIO(png_bytes))

        self.pda_plot = Matplotlib_Popup_Window(parent = self, img=img, title='PDA')
        self.pda_plot.show()
        self.pda_plot.center()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
    def closeAndReturn(self):
        self.close()
        self.parent().show()
    
    def closeEvent(self, event):
        self.closeAndReturn()
        event.accept()
