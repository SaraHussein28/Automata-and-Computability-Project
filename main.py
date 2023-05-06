from tkinter import *
from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QWidget, QHBoxLayout, QVBoxLayout
import Grammar.grammarImport as Grammar
from cfgToPda import Automaton
import matplotlib.pyplot as plt
import graphviz

from convertToGNF import convertToGNF
from convertToGNF import generate_gnf_grammar

G = graphviz.Digraph('finite_state_machine', comment='The Round Table')
G.attr(rankdir='LR', size='8,5')


def submit():
    input = text_edit.toPlainText()
    productions = Grammar.importGrammar(input)
  
    gnf = convertToGNF(productions)
    print (gnf)
    states, transitions = Grammar.generate_states_and_transitions(gnf)
    pda = Automaton(states, transitions)
    res = pda.toPda()
    print (res)
    show_pda(res=res)

    res = generate_gnf_grammar(productions)
    show_gnf(gnf=res)
    generate_graph(transitions=transitions)
    draw()
    grammar_status_label.setText("submitted")   



def draw():
    print (G)

    plt.show()




def show_pda(res):
    pda_grammar.setPlainText(res)
    
def show_gnf(gnf):
    gnf_grammar.setPlainText(gnf)

def generate_graph(transitions):
    graph_list = dict()
    G.node('Q0')
    G.node('Q1')
    G.node('Q2')
    for transition in transitions:

        src, dst = transition.currState.__str__(), transition.nextState.__str__()
        print (src , "   ", dst)
        G.edge(src, dst, label=transition.__str__())
        #G.add_edge(src, dst, w=transition.__str__(),color = "black")
        if (src,dst) not in graph_list:
            graph_list[(src,dst)] = list()
        graph_list[(src,dst)].append(transition.__str__())
    
    print(graph_list)
    G.view()
    
    return graph_list


# ###
# key pair(q1, q2)
# value = ["a,pop symbol -> push symbol", ....]
# ###
            

        


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


subgrid = QHBoxLayout()
subgrid.addWidget(text_edit)
subgrid.addWidget(gnf_grammar)
subgrid.addWidget(pda_grammar)


grid.addLayout(labels_subgrid)
grid.addLayout((subgrid))
grid.addWidget(grammar_status_label)

grid.addWidget(submit_button)


main_widget.setFixedSize(900, 500)

main_widget.setWindowTitle('Lexer')
main_widget.setLayout(grid)
main_widget.show()

app.exec()


# fig = plt.figure()
# canvas = FigureCanvasTkAgg(fig, GraphInputPage)
# canvas.draw()
# canvas.get_tk_widget().pack(side=RIGHT, fill=Y)
# GraphInputPage.mainloop()