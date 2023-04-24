from PyQt5.QtWidgets import QApplication, QPushButton, QLabel, QTextEdit, QWidget, QTableWidget, QTableWidgetItem, QHBoxLayout, QVBoxLayout
import Grammar.grammarImport as Grammar
from cfgToPda import Automaton

def submit():
    input = text_edit.toPlainText()
    states, transitions = Grammar.importGrammar(input)
    pda = Automaton(states, transitions)
    res = pda.toPda()
    print (res)
    show_pda(res=res)
    graph_list = generate_graph(transitions=transitions)
    grammar_status_label.setText("submitted")   


def show_pda(res):
    pda_grammar.setPlainText(res)
    

def generate_graph(transitions):
    graph_list = dict()

    for transition in transitions:

        src, dst = transition.currState.__str__(), transition.nextState.__str__()
        print (src , "   ", dst)
        if (src,dst) not in graph_list:
            graph_list[(src,dst)] = list()
        graph_list[(src,dst)].append(transition.__str__())
    
    print(graph_list)
    return graph_list


# ###
# key pair(q1, q2)
# value = ["a,pop symbol -> push symbol", ....]
# ###
            

        




app = QApplication([])
main_widget = QWidget()

text_edit = QTextEdit()
text_edit.setTabStopWidth(15)
input_label = QLabel('Enter Context Free Grammar below !')

grammar_status_label = QLabel("Status: Waiting...")
submit_button = QPushButton('Submit')
submit_button.clicked.connect(submit)



pda_grammar = QTextEdit()
pda_grammar.setTabStopWidth(15)
pda_grammar.setReadOnly(True)
pda_label = QLabel('PDA grammar')


grid = QVBoxLayout()

labels_subgrid = QHBoxLayout()
labels_subgrid.addWidget(input_label)
labels_subgrid.addWidget(pda_label)


subgrid = QHBoxLayout()
subgrid.addWidget(text_edit)
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