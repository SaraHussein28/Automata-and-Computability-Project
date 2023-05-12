from collections import defaultdict
import graphviz
from itertools import combinations
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

class Minimal_DFA(DFA):
    def __init__(self, dfa :DFA) -> None:
        self.automata = dfa.automata
        self.alphabet = dfa.alphabet
        self.final_states = dfa.final_states
        self.start_state = dfa.start_state
        self.transition_table = self.generateTransitionTable()
        self.minimize()
    
    def generateTransitionTable(self):
        transitionTable = {}
        for state,transitions in self.automata.items():
            transitionTable[state] = {character: None for character in sorted(self.alphabet)}
            for transition in transitions:
                destNode = transition["destination"]
                transition_condition = transition["transition"]
                transitionTable[state][transition_condition] = destNode
        print("Transition Table: ",transitionTable,'\n\n')
        return transitionTable
    
    def getInitialPartitions(self):
        non_final_states = set(list(self.automata.keys()))
        final_states = set(map(tuple,self.final_states))
        non_final_states.difference_update(final_states)
        partition = set([frozenset(non_final_states),frozenset(final_states)])
        return partition
    
    def getTransitionSet(self, state, partitions, character):
        transition_state = self.transition_table[state][character]
        if transition_state == None:
            return None
        for set in partitions:
            if tuple(transition_state) in set:
                return set

    def divide(self, partition, last_partitions):
        partition = list(partition)
        if len(partition) == 0:
            return [set()]
        tempset=set()
        tempset.add(partition[0])
        sub_partitions = [tempset]
        for state in partition[1:]:
            equivalent = False
            for sub_partition in sub_partitions:
                state1 = next(iter(sub_partition)) #get an arbitrary state from the current sub_partition
                equivalent = True
                for character in self.alphabet:
                    state_transition_set = self.getTransitionSet(state=state, partitions=last_partitions, character=character)
                    state1_transition_set = self.getTransitionSet(state=state1, partitions=last_partitions, character=character)
                    if state_transition_set != state1_transition_set:
                        equivalent = False
                        break
                if equivalent:
                    sub_partition.add(tuple(state))
                    break
            if equivalent == False:
                sub_partitions.append(set([tuple(state)]))
        return sub_partitions
    
    def getNextPartitions(self, partitions):
        next_partitions = []
        for partition in partitions:
            temp = self.divide(partition=partition, last_partitions = partitions)
            next_partitions.extend(temp)
        return set({frozenset(set) for set in next_partitions})
    
    def generateStateFromPartition(self, partition):
        state = []
        for sub_state in partition:
            state.extend(sub_state)
        state = list(set(state))
        state.sort()
        return tuple(state)

    def updateAutomata(self, partitions):
        self.automata.clear()
        for partition in partitions:
            if len(partition)==0:
                continue
            src_state = self.generateStateFromPartition(partition=partition)
            self.add_state(state_name=src_state)
            for state in partition:
                if list(state) == self.start_state:
                    self.set_start_state(state=list(src_state))
                if state in self.final_states:
                    self.add_final_state(state=src_state)

            selected_state = list(partition)[0] #select an arbitrary state from the partition
            for character in self.alphabet:
                dest_set = self.getTransitionSet(state=selected_state, partitions=partitions, character=character)
                if dest_set:
                    dest_state = self.generateStateFromPartition(partition=dest_set)
                    self.add_transition(src_state=src_state, dest_state=dest_state, condition=character)

        print("minimized automata:", self.automata)


    def minimize(self):
        prev_partitions = self.getInitialPartitions()
        print("initial partitions:", prev_partitions)
        while True:
            next_partitions = self.getNextPartitions(partitions = prev_partitions)
            if next_partitions == prev_partitions:
                print("Final partitions:", prev_partitions)
                break
            prev_partitions = next_partitions
        self.updateAutomata(partitions=prev_partitions)

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
        print(f"{node} epsilon Closure: {e_closure}")
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
            for sub_state in state:
                if sub_state in self.final_states and state not in dfa.final_states:
                    dfa.final_states.append(state)
            for transition in self.alphabet:
                temp = []
                for sub_state in state:
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
