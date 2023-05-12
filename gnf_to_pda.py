import Utils.constants as constant
from Automata.transition import Transition
from Automata.state import State

def convert_to_PDA(grammar):
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
    init = Transition(constant.LAMBDA, initState, midState, constant.EMPTY_STACK, ["S", constant.EMPTY_STACK])    
    transitions.append(init)
    # final state transition upon encountering epsilon
    final = Transition(constant.LAMBDA, midState, finalState, constant.EMPTY_STACK, [constant.EMPTY_STACK])
    transitions.append(final)
    return transitions
