from tkinter import *
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout
import IO as Grammar
import matplotlib.pyplot as plt
import graphviz

from cfg_to_gnf import convertToGNF
from gnf_to_pda import convert_to_PDA

G = graphviz.Digraph('finite_state_machine', comment='The Round Table')
G.attr(rankdir='LR', size='8,5')


def submit():
    input = text_edit.toPlainText()
    grammar = Grammar.parse_input_grammar(input)
  
    gnf = convertToGNF(grammar)

    
    print (gnf)
    transitions = convert_to_PDA(gnf)
    res = Grammar.build_PDA_output(transitions)
    print (res)
    show_pda(res=res)

    res = Grammar.build_gnf_grammar_output(grammar)
    show_gnf(gnf=res)
    graph, graph_list = Grammar.build_graph_output(G = G, transitions=transitions)
    graph.view()
    plt.show()
    grammar_status_label.setText("Status: submitted")   



def show_pda(res):
    pda_grammar.setPlainText(res)
    
def show_gnf(gnf):
    gnf_grammar.setPlainText(gnf)




app = QApplication([])
main_widget = QWidget()

text_edit = QTextEdit()
text_edit.setTabStopWidth(15)
input_label = QLabel('Enter Context Free Grammar below!')

grammar_status_label = QLabel("Status: Waiting...")
submit_button = QPushButton('Submit')
submit_button.clicked.connect(submit)


gnf_grammar = QTextEdit()
gnf_grammar.setTabStopWidth(15)
gnf_grammar.setReadOnly(True)

pda_grammar = QTextEdit()
pda_grammar.setTabStopWidth(15)
pda_grammar.setReadOnly(True)

gnf_label = QLabel('GNF')
pda_label = QLabel('PDA grammar')



grid = QVBoxLayout()

labels_subgrid = QHBoxLayout()
labels_subgrid.addWidget(input_label)
labels_subgrid.addWidget(gnf_label)
labels_subgrid.addWidget(pda_label)


textboxes_subgrid = QHBoxLayout()
textboxes_subgrid.addWidget(text_edit)
textboxes_subgrid.addWidget(gnf_grammar)
textboxes_subgrid.addWidget(pda_grammar)


grid.addLayout(labels_subgrid)
grid.addLayout((textboxes_subgrid))
grid.addWidget(grammar_status_label)

grid.addWidget(submit_button)


main_widget.setFixedSize(900, 500)

main_widget.setWindowTitle('CFG to PDA')
main_widget.setLayout(grid)
main_widget.show()

app.exec()