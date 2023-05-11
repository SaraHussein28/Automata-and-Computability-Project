
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

        self.text_edit = QTextEdit()
        self.text_edit.setTabStopWidth(15)
        self.input_label = QLabel('Enter Context Free Grammar below!')

        self.grammar_status_label = QLabel("Status: Waiting...")
        self.submit_button = QPushButton('Submit')
        self.submit_button.clicked.connect(self.submit)


        self.gnf_grammar = QTextEdit()
        self.gnf_grammar.setTabStopWidth(15)
        self.gnf_grammar.setReadOnly(True)

        self.pda_grammar = QTextEdit()
        self.pda_grammar.setTabStopWidth(15)
        self.pda_grammar.setReadOnly(True)

        self.gnf_label = QLabel('GNF')
        self.pda_label = QLabel('PDA grammar')



        grid = QVBoxLayout()

        labels_subgrid = QHBoxLayout()
        labels_subgrid.addWidget(self.input_label)
        labels_subgrid.addWidget(self.gnf_label)
        labels_subgrid.addWidget(self.pda_label)


        textboxes_subgrid = QHBoxLayout()
        textboxes_subgrid.addWidget(self.text_edit)
        textboxes_subgrid.addWidget(self.gnf_grammar)
        textboxes_subgrid.addWidget(self.pda_grammar)


        grid.addLayout(labels_subgrid)
        grid.addLayout((textboxes_subgrid))
        grid.addWidget(self.grammar_status_label)

        grid.addWidget(self.submit_button)


        main_widget.setFixedSize(900, 500)
        main_widget.setLayout(grid)
        self.setCentralWidget(main_widget)
        self.setWindowTitle('CFG to PDA converter')
    
    def show_pda(self, res):
        self.pda_grammar.setPlainText(res)
        
    def show_gnf(self, gnf):
        self.gnf_grammar.setPlainText(gnf)

    def submit(self):
        G = graphviz.Digraph('finite_state_machine', comment='The Round Table')
        G.attr(rankdir='LR', size='8,5')
        input = self.text_edit.toPlainText()
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
        
        self.grammar_status_label.setText("Status: submitted")

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