from Utils.Exceptions import IllegalVariableException
import Utils.constants as constant
from Automata.state import State
from Automata.transition import Transition


def generate_states_and_transitions(grammar):
    initState = State("Q0", True, False, [])
    midState = State("Q1", False, False, [])
    finalState = State("Q2", False, True, [])

    transitions = []
    for key in grammar:
        for production in grammar[key]:
            trans = Transition(
                production[:1], #terminal
                midState,
                midState,
                key, #pop rule symbol on transition ---> lhs = key
                # bn consume awel char (elly howa dayman terminal because GNF) and push elly b3d el terminal dah
                list(production[1:]) if len(list(production[1:])) > 0 else [constant.LAMBDA]
            )
            transitions.append(trans)
    
        # initial state & transition
    init = Transition(constant.LAMBDA, initState, midState, constant.EPSILON, ["S", constant.EPSILON])    
    transitions.append(init)
    # final state transition upon encountering epsilon
    final = Transition(constant.LAMBDA, midState, finalState, constant.EPSILON, [constant.EPSILON])
    transitions.append(final)
    states = [initState, midState, finalState]
    return states, transitions


def importGrammar (input):

    data = input.splitlines()
    print(data)
    
    transitions = []
    initStateSym = data[0].rstrip()
    
    terminals = data[1].rstrip()
    
    initState = State("Q0", True, False, [])
    midState = State("Q1", False, False, [])
    finalState = State("Q2", False, True, [])
    
    terminals = terminals.split(',')
    productions = {}
    
    for idx in range(2, data.__len__()):
        rule = data[idx].strip()
        rule = rule.replace(" ", "")
        for character in rule:
            if character == '-' or character == '>' or character == '|':
                pass
            elif character not in terminals and (not character.isupper()) and character != constant.LAMBDA:
                raise IllegalVariableException(character, rule)
        
        #left hand side: state        
        lhs = rule[:rule.find('-')]
        if lhs not in productions:
            productions[lhs] = []
        #right hand side: productions
        rhs = rule[rule.find('>') + 1:]
        #split productions
        rhs = rhs.split('|')
        print (rhs)
        #assign productions to each state
        for t in rhs:
            productions[lhs].append(t)
            trans = Transition(
                t[:1], #terminal
                midState,
                midState,
                lhs, #pop rule symbol on transition ---> lhs = key
                # bn consume awel char (elly howa dayman terminal because GNF) and push elly b3d el terminal dah
                list(t[1:]) if len(list(t[1:])) > 0 else [constant.LAMBDA]
            )
            transitions.append(trans)

    # initial state & transition
    init = Transition(constant.LAMBDA, initState, midState, constant.EPSILON, [initStateSym, constant.EPSILON])    
    transitions.append(init)
    # final state transition upon encountering epsilon
    final = Transition(constant.LAMBDA, midState, finalState, constant.EPSILON, [constant.EPSILON])
    transitions.append(final)
    states = [initState, midState, finalState]
    #return states, transitions, productions
    return productions
