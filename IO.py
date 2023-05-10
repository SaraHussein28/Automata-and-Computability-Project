from Utils.Exceptions import IllegalVariableException
import Utils.constants as constant

def build_graph_output(G, transitions):
    graph_list = dict()
    G.node('Q0')
    G.node('Q1')
    G.node('Q2')
    for transition in transitions:

        src, dst = transition.currState.__str__(), transition.nextState.__str__()
        print (src , "   ", dst)
        G.edge(src, dst, label=transition.__str__())
        if (src,dst) not in graph_list:
            graph_list[(src,dst)] = list()
        graph_list[(src,dst)].append(transition.__str__())
    
    print(graph_list)
    
    
    return G, graph_list

def build_PDA_output(transitions):
    trFunc = {}
    res = "Transitions:"
    for t in transitions:
        key = (t.currState, t.inputSymbol, t.popSymbol)
        # make a new key in transition function if not found
        if (not key in trFunc.keys()):
            trFunc[key] = []
        trFunc[key].append((t.nextState, t.pushSymbols))
    trFunc = enumerate(trFunc.items())
    for i, (key, value) in trFunc:
        res += '\n'
        res += str(constant.DELTA) + '(' + str(key[0]) + ',' +str (key[1]) + ',' + str(key[2]) + ') = { '

        targets = []
        for val in value:
            pushStr = ''.join(val[1])
            targets.append(
                '(' + str(val[0]) + ',' + pushStr + ')'
            )
        res += str(', ').join(targets) + ' }'
    
    return res




def parse_input_grammar (input):


    data = input.splitlines()


    terminals = data[1].rstrip()
    
    
    terminals = terminals.split(',')
    grammar = {}
    
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
        if lhs not in grammar:
            grammar[lhs] = []

        #right hand side: productions
        rhs = rule[rule.find('>') + 1:]

        #split productions
        rhs = rhs.split('|')

        #assign productions to each state
        for t in rhs:
            grammar[lhs].append(t)


    return grammar


def build_gnf_grammar_output(grammar):
    res = ""
    terminals = ""
    transtions = ""
    first = True

    for key in grammar:
        for production in grammar[key]:
            
            for pr in production:
                if pr.islower() and pr not in terminals:
                    terminals+=pr + ','

    res = 'S' +'\n' + terminals +'\n'
    
    for key in grammar:
        for production in grammar[key]:
            
            if not first:
                transtions+= '|' + production
            else:
                transtions+= key + ' -> ' + production
                first = False
        first = True


        transtions +='\n'
    res+= transtions
    return res