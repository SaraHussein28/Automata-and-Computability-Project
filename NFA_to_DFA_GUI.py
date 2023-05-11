from PyQt5 import QtCore
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QApplication,
    QMainWindow,
    QPushButton,
    QLabel,
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QLineEdit,
    QComboBox,
    QMessageBox,
    QGroupBox
)

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg

import io

from NFA_to_DFA_Logic import NFA, DFA, Finite_automata

class NFA_To_DFA_Converter(QMainWindow):
    def __init__(self, parent):
        super(NFA_To_DFA_Converter, self).__init__(parent)
        # ensure this window gets garbage-collected when closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        self.num_states = 0

        self.main_widget = QWidget()
        self.nfa_figure = Figure()
        self.nfa_plot = self.nfa_figure.add_subplot(111)
        self.nfa_plot.axis('off')
        self.nfa_plot_widget = FigureCanvasQTAgg(figure=self.nfa_figure)
        nfa_plot_layout = QHBoxLayout()
        nfa_plot_layout.addWidget(self.nfa_plot_widget)

        self.dfa_figure = Figure()
        self.dfa_plot = self.dfa_figure.add_subplot(111)
        self.dfa_plot.axis('off')
        self.dfa_plot_widget = FigureCanvasQTAgg(figure=self.dfa_figure)
        dfa_plot_layout = QHBoxLayout()
        dfa_plot_layout.addWidget(self.dfa_plot_widget)

        self.nfa = NFA()

        addStates_layout = QVBoxLayout()
        self.stateName_lbl = QLabel('Enter state name:')
        self.stateName_txtBox = QLineEdit()
        self.stateName_txtBox.setText(f'q{self.num_states}')
        self.addState_btn = QPushButton('Add state')
        self.addState_btn.clicked.connect(self.add_state)
        addStates_layout.addWidget(self.stateName_lbl)
        addStates_layout.addWidget(self.stateName_txtBox)
        addStates_layout.addWidget(self.addState_btn)
        addStates_groupBox = QGroupBox('Add State')
        addStates_groupBox.setLayout(addStates_layout)

        addTransition_layout = QVBoxLayout()
        self.srcState_lbl = QLabel('Source state:')
        self.srcState_combobox = QComboBox()
        self.dstState_lbl = QLabel('Destination state:')
        self.dstState_combobox = QComboBox()
        self.transitionCondition_lbl = QLabel('Transition condition: (leave empty for epsilon)')
        self.transitionCondition_txtBox = QLineEdit()
        self.addTransition_btn = QPushButton('Add transition')
        self.addTransition_btn.clicked.connect(self.add_transition)
        addTransition_layout.addWidget(self.srcState_lbl)
        addTransition_layout.addWidget(self.srcState_combobox)
        addTransition_layout.addWidget(self.dstState_lbl)
        addTransition_layout.addWidget(self.dstState_combobox)
        addTransition_layout.addWidget(self.transitionCondition_lbl)
        addTransition_layout.addWidget(self.transitionCondition_txtBox)
        addTransition_layout.addWidget(self.addTransition_btn)
        addTransition_groupBox = QGroupBox('Add transition')
        addTransition_groupBox.setLayout(addTransition_layout)

        initialState_layout = QVBoxLayout()
        self.initialState_combobox = QComboBox()
        self.setInitialState_btn = QPushButton('Set initial state')
        self.setInitialState_btn.clicked.connect(self.setInitialState)
        initialState_layout.addWidget(self.initialState_combobox)
        initialState_layout.addWidget(self.setInitialState_btn)
        start_state_groupBox = QGroupBox('Initial state')
        start_state_groupBox.setLayout(initialState_layout)


        final_state_layout = QVBoxLayout()
        self.finalState_combobox = QComboBox()
        self.addFinalState_btn = QPushButton('Add final state')
        self.addFinalState_btn.clicked.connect(self.addFinalState)
        final_state_layout.addWidget(self.finalState_combobox)
        final_state_layout.addWidget(self.addFinalState_btn)
        final_state_groupbox = QGroupBox('Add final state')
        final_state_groupbox.setLayout(final_state_layout)

        self.clear_btn = QPushButton('Clear automata')
        self.clear_btn.clicked.connect(self.clear_automata)

        controls_layout = QVBoxLayout()
        controls_layout.addWidget(addStates_groupBox)
        controls_layout.addWidget(addTransition_groupBox)
        controls_layout.addWidget(start_state_groupBox)
        controls_layout.addWidget(final_state_groupbox)
        controls_layout.addWidget(self.clear_btn)

        plots_layout = QVBoxLayout()
        nfa_groupBox = QGroupBox('NFA')
        dfa_groupBox = QGroupBox('DFA')
        nfa_groupBox.setLayout(nfa_plot_layout)
        dfa_groupBox.setLayout(dfa_plot_layout)
        plots_layout.addWidget(nfa_groupBox)
        plots_layout.addWidget(dfa_groupBox)

        grid = QHBoxLayout()
        grid.addLayout(controls_layout)
        grid.addLayout(plots_layout)

        self.main_widget.setLayout(grid)
        self.setCentralWidget(self.main_widget)
        self.setWindowTitle('NFA to DFA converter')
        self.disable_buttons()
    
    def update_plot(self, automata: Finite_automata, plot: plt.Axes):
        G = automata.get_Graph()
        png_bytes = G.pipe(format='png')

        img = plt.imread(io.BytesIO(png_bytes))
        plot.clear()
        plot.imshow(img)
        plot.axis('off')

    def update_DFA_plot(self, dfa: DFA):
        self.update_plot(automata=dfa, plot=self.dfa_plot)
        self.dfa_plot_widget.draw()

    def update_NFA_plot(self):
        self.update_plot(automata=self.nfa, plot=self.nfa_plot)
        self.nfa_plot_widget.draw()
    
    def update_plots(self):
        self.update_NFA_plot()
        self.convert_to_dfa()

    def update_comboboxes(self):
        states = list(self.nfa.automata.keys())
        self.srcState_combobox.clear()
        self.srcState_combobox.addItems(states)
        self.dstState_combobox.clear()
        self.dstState_combobox.addItems(states)
        self.initialState_combobox.clear()
        self.initialState_combobox.addItems(states)
        self.finalState_combobox.clear()
        self.finalState_combobox.addItems(states)

    def add_state(self):
        name = self.stateName_txtBox.text()

        if len(name) == 0:
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Critical)
            msg.setText("Error")
            msg.setInformativeText('State name cannot be empty')
            msg.setWindowTitle("Error")
            msg.exec_()
            return
        if self.num_states == 0:
            self.nfa.set_start_state(state=name)
            self.enable_buttons()
        self.num_states+=1
        self.nfa.add_state(state_name=name)
        self.stateName_txtBox.setText(f'q{self.num_states}')
        self.update_comboboxes()
        self.update_plots()

    def add_transition(self):
        src_state = self.srcState_combobox.currentText()
        dst_state = self.dstState_combobox.currentText()
        transition = self.transitionCondition_txtBox.text()
        self.nfa.add_transition(src_state=src_state, dest_state=dst_state, condition=transition)
        self.update_plots()
                
    def setInitialState(self):
        state = self.initialState_combobox.currentText()
        self.nfa.set_start_state(state=state)
        self.update_plots()

    def addFinalState(self):
        state = self.finalState_combobox.currentText()
        self.nfa.add_final_state(state=state)
        self.update_plots()

    def convert_to_dfa(self):
        dfa = self.nfa.generateDFA()
        self.update_DFA_plot(dfa=dfa)

    def clear_automata(self):
        self.nfa = NFA()
        dfa = DFA()
        self.update_NFA_plot()
        self.update_DFA_plot(dfa = dfa)
        self.update_comboboxes()
        self.num_states = 0
        self.stateName_txtBox.setText(f'q{self.num_states}')
        self.disable_buttons()

    def disable_buttons(self):
        self.addTransition_btn.setDisabled(True)
        self.setInitialState_btn.setDisabled(True)
        self.addFinalState_btn.setDisabled(True)
    
    def enable_buttons(self):
        self.addTransition_btn.setEnabled(True)
        self.setInitialState_btn.setEnabled(True)
        self.addFinalState_btn.setEnabled(True)

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