
import Utils.constants as constant

def simplify_grammar(grammar):
    print ("Removing Lamda")
    grammar = remove_lamda_productions(grammar)
    print (grammar)

    print("removing unit productions")
    remove_unit_productions(grammar)
    print(grammar)

    print ("Removing Non accessible")
    grammar = remove_non_accessible(grammar)
    print(grammar)

    print ("Removing Non productive")
    grammar = remove_non_productive(grammar)
    print (grammar)

    return grammar


def make_permutations(rule, nonterm):
    rule_lst = []
    alredy_added = []
    count = 0
    new_set = set()

    for letter in rule:
        if letter != nonterm:
            rule_lst.append(letter)
        elif letter == nonterm:
            rule_lst.append(letter)
            count += 1

    if count == 1 and nonterm in rule_lst:
        original = "".join(rule_lst)
        making = [x for x in rule_lst if x != nonterm]
        new = "".join(making)
        alredy_added.append(new)
        alredy_added.append(original)
        if (original != ''):
            new_set.add(original)
        if (new != ''):
            new_set.add(new)        
        

    if count == 0 and nonterm not in rule_lst:
        making = [x for x in rule_lst if x != nonterm]
        new = "".join(making)
        alredy_added.append(new)
        new_set.add(new)
    if count == len(rule_lst):
        new_set.add(constant.EPSILON)
        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)
        for i in range(count):
            new = i*nonterm
            if new not in alredy_added:
                alredy_added.append(new)
                new_set.add(new)
    if count > 1:

        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)

        without_nonterminals = "".join([x for x in rule_lst if x != nonterm])
        alredy_added.append(without_nonterminals)
        new_set.add(without_nonterminals)

        index = 0
        for i in rule_lst:
            if i == nonterm:
                before = "".join(rule_lst[:index])
                if before == "":
                    before = ''
                after = "".join(rule_lst[index+1:])
                new = before + after
                if new not in alredy_added:
                    alredy_added.append(new)
                    new_set.add(new)
                before = "".join([x for x in rule_lst[:index] if x != nonterm])
                after = "".join(
                    [x for x in rule_lst[index+1:] if x != nonterm])
                
                new = before + nonterm + after
                if new not in alredy_added:
                    alredy_added.append(new)
                    new_set.add(new)
                index += 1
            if i != nonterm:
                index += 1

    return list(new_set)




def remove_lamda_productions(grammar):
    gram = copy_grammar(grammar)

    keys = []
    for key in gram:
        keys.append(key)

    for key in keys:
        if constant.EPSILON not in gram[key]:
            continue
        nonterm = key
        for key in gram.keys():
            for value in gram[key]:
                if nonterm in value:
                    new_value = make_permutations(value, nonterm)
                    for i in new_value:
                        if i not in gram[key]:
                            gram[key].append(i)
        if constant.EPSILON in gram[nonterm]:
            gram[nonterm].remove(constant.EPSILON)
    
    for key in gram:
        for value in gram[key]:
            if value ==  constant.EPSILON:
                gram[key].remove(constant.EPSILON)
    return gram


def copy_grammar(grammar):
    grammar_copy = dict()
    for key, production in grammar.items():
        grammar_copy[key] = production.copy()
    return grammar_copy





def remove_unit_productions(grammar):
    unitProductions = getUnitProductions(grammar)
    print("Unit Productions = ", unitProductions)
        # remove unit productions

    for key in unitProductions:
        for production in unitProductions[key]:
            if grammar[key].__contains__(production):
                grammar[key].remove(production)

    for key in unitProductions:
        for production in unitProductions[key]:
            grammar[key].extend(set(grammar[production]) - set(grammar[key]))


visUnit = set()
def checkForMultipleUnitProductions(unitProductions, key):
    if not unitProductions[key][0] in unitProductions or key in visUnit:
        return unitProductions[key][0]
    visUnit.add(key)
    return checkForMultipleUnitProductions(unitProductions, unitProductions[key][0])

def getUnitProductions(grammar):
    unitProductions = {}
    for key in grammar:
        temp = []
        for production in grammar[key]:
            if len(production) == 1 and production.isupper():
                temp.append(production)
        if temp:
            unitProductions[key] = temp

    for key in unitProductions:
        temp = checkForMultipleUnitProductions(unitProductions, key)
        if temp and temp != key and temp not in unitProductions[key]:
            unitProductions[key].extend(temp)

    return unitProductions

def checkAccesible(productions, start, accessible):
    if start != "S":
        if start in accessible:
            return
        elif start not in accessible:
            accessible.extend(start)

    for production in productions[start]:
        for char in production:
            if char.isupper() and char != start and char not in accessible:
                accessible = checkAccesible(productions, char, accessible)

    return accessible

def remove_non_accessible(productions):
    accesible = ["S"]
    accesible = checkAccesible(productions, "S", accesible)
    
    nonTerminals = set(productions.keys())
    nonAccesible = set(nonTerminals) - set(accesible)
    print("Non Accesible = ", nonAccesible)
    for key in nonAccesible:
        productions.pop(key)
    
    return productions

def getNonProductiveSymbols(grammar):
    nonTerminals = set(grammar.keys())
    productiveSymbols = set()
    for key in grammar:
        if any(production.islower() for production in grammar[key]):
            productiveSymbols.add(key)

    # if a NonTerminal 2 NonTerminals in productions, they could be productive or not productive
    temp = nonTerminals.difference(productiveSymbols)
    temp2 = {""}
    for key in grammar:
        for production in grammar[key]:
            for productive in productiveSymbols:
                if production.__contains__(productive):
                    for nonProductive in temp:
                        if not production.__contains__(nonProductive):
                            temp2.add(key)

    productiveSymbols |= (temp2)

    return list(nonTerminals.difference(productiveSymbols))

def remove_non_productive(grammar):
    nonProductiveSymbols = getNonProductiveSymbols(grammar)
    print("Non Productive Set = ", nonProductiveSymbols)
    if not nonProductiveSymbols:
        return grammar
    for key in grammar:
        for production in grammar[key]:
            for nonProductive in nonProductiveSymbols:
                if production.__contains__(nonProductive):
                    grammar[key].remove(production)
    
    for symbol in nonProductiveSymbols:
        grammar.pop(symbol)

    return grammar
