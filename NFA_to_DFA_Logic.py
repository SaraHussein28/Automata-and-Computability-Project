from collections import defaultdict
import graphviz
from Utils.constants import EPSILON

class Finite_automata():
    automata = None
    start_state = None
    final_states = None
    alphabet = None

    def __init__(self) -> None:
        self.automata = {}
        self.final_states = []
        self.alphabet = set()

    def add_state(self, state_name):
        self.automata[state_name] = []

    def add_transition(self, src_state, dest_state, condition):
        if condition == '':
            condition = EPSILON
        transition = {"destination": dest_state, "transition": condition}
        if transition in self.automata[src_state]:
            return
        self.automata[src_state].append(transition)
        if condition != EPSILON:
            self.alphabet.add(condition)

    def set_start_state(self, state):
        self.start_state = state

    def add_final_state(self, state):
        self.final_states.append(state)
        self.final_states = list(set(self.final_states))


class DFA(Finite_automata):
    def __init__(self) -> None:
        super().__init__()
    
    def has_state(self, state):
        return self.automata.get(state)
    
    def minimize(self):
        pass

    def check(self, input_string):
        #should return true if the input string is accepted and false otherwise
        pass

    def get_Graph(self):
        G = graphviz.Digraph()
        G.attr(rankdir='LR')
        G.attr(dpi = "400")
        if self.start_state:
            #invisible node for the tail of the arrow going to the starting state
            G.node(name="hidden_node",label="", shape = 'point', width = '0', height= '0')
        
        #create nodes
        for state, _ in self.automata.items():
            state_name = ', '.join(state)
            G.node(name=state_name, shape = 'circle')
            if(list(state) in self.final_states):
                G.node(name=state_name, shape = 'doublecircle')
            
            if(list(state) == self.start_state):
                G.edge(tail_name="hidden_node", head_name=state_name)

        #add edges
        for state, transitions in self.automata.items():
            for transition in transitions:
                src = ', '.join(state)
                dest = ', '.join(transition["destination"])
                label = transition["transition"]
                G.edge(tail_name=src, head_name=dest, label=label)
        
        return G


class NFA(Finite_automata):
    epsilon_closure = None

    def __init__(self) -> None:
        super().__init__()
        self.epsilon_closure = {}

    def dfs(self, node, visited):
        visited[node] = True
        e_closure = set()
        e_closure.add(node)
        for child in self.automata[node]:
            if child["transition"] == EPSILON and visited[child["destination"]] == False:
                temp = self.dfs(child["destination"], visited)
                e_closure.update(temp)
        return e_closure

    def computeEpsilonClosure(self):
        for key,val in self.automata.items():
            visited = defaultdict(lambda: False)
            e_closure = self.dfs(node=key, visited=visited)
            e_closure = list(e_closure)
            e_closure.sort()
            self.epsilon_closure[key] = e_closure
    
    def generateDFA(self):
        self.computeEpsilonClosure()
        starting_state = self.epsilon_closure[self.start_state]
        pending_states = []
        pending_states.append(starting_state)
        dfa = DFA()
        dfa.set_start_state(state = starting_state)

        while(len(pending_states)):
            state = pending_states[0]
            del pending_states[0]
            if dfa.has_state(state=tuple(state)):
                continue
            dfa.add_state(tuple(state))
            for transition in self.alphabet:
                temp = []
                for sub_state in state:
                    if sub_state in self.final_states and state not in dfa.final_states:
                        dfa.final_states.append(state)
                    for child in self.automata[sub_state]:
                        if(child["transition"] !=  transition):
                            continue
                        temp.extend(self.epsilon_closure[child["destination"]])
                temp = list(set(temp))
                temp.sort()
                if len(temp):
                    dfa.add_transition(src_state=tuple(state), dest_state=temp, condition=transition)
                    # dfa[tuple(state)].append({"destination":temp, "transition":transition})
                    pending_states.append(temp)
        return dfa
    
    def get_Graph(self):
        G = graphviz.Digraph()
        G.attr(rankdir='LR')
        G.attr(dpi = "400")
        if self.start_state:
            #invisible node for the tail of the arrow going to the starting state
            G.node(name="hidden_node",label="", shape = 'point', width = '0', height= '0')
        #create nodes
        for state, _ in self.automata.items():
            state_name = state
            G.node(name=state_name, shape = 'circle')
            if(state in self.final_states):
                G.node(name=state_name, shape = 'doublecircle')
            
            if(state == self.start_state):
                G.edge(tail_name="hidden_node", head_name=state_name)

        #add edges
        for state, transitions in self.automata.items():
            for transition in transitions:
                src = state
                dest = transition["destination"]
                label = transition["transition"]
                G.edge(tail_name=src, head_name=dest, label=label)
        
        return G
