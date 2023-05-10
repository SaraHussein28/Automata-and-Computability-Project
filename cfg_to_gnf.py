import string
import Utils.constants as constant


def convertToGNF(grammar):
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
    grammar = removeNonProductive(grammar)
    print (grammar)

    normalizeToChomsky(grammar)
    normalizeToGreibach(grammar)

    print ("Removing Non accessible")
    grammar = remove_non_accessible(grammar)
    print(grammar)

    print ("Removing Non productive")
    grammar = removeNonProductive(grammar)
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
    print(rule_lst)

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
        
    print("here1 ", new_set)

    if count == 0 and nonterm not in rule_lst:
        making = [x for x in rule_lst if x != nonterm]
        new = "".join(making)
        alredy_added.append(new)
        new_set.add(new)
    print("here2 ", new_set)
    if count == len(rule_lst):
        new_set.add(constant.LAMBDA)
        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)
        print("here45 ", new_set)
        for i in range(count):
            new = i*nonterm
            if new not in alredy_added:
                alredy_added.append(new)
                new_set.add(new)
                print("here46 ", new_set)
    print("here3 ", new_set)
    if count > 1:

        original = "".join(rule_lst)
        alredy_added.append(original)
        new_set.add(original)

        without_nonterminals = "".join([x for x in rule_lst if x != nonterm])
        alredy_added.append(without_nonterminals)
        new_set.add(without_nonterminals)
        print("here4 ", new_set)

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
                print("here5 ", new_set)
                before = "".join([x for x in rule_lst[:index] if x != nonterm])
                after = "".join(
                    [x for x in rule_lst[index+1:] if x != nonterm])
                
                new = before + nonterm + after
                if new not in alredy_added:
                    alredy_added.append(new)
                    new_set.add(new)
                print("here6 ", new_set)
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
        if constant.LAMBDA not in gram[key]:
            continue
        nonterm = key
        for key in gram.keys():
            for value in gram[key]:
                if nonterm in value:
                    new_value = make_permutations(value, nonterm)
                    print(new_value)
                    for i in new_value:
                        if i not in gram[key]:
                            gram[key].append(i)
        print("print1 ", gram)
        if constant.LAMBDA in gram[nonterm]:
            print ("here")
            gram[nonterm].remove(constant.LAMBDA)
    
    print("print2 ",gram)
    for key in gram:
        for value in gram[key]:
            if value ==  constant.LAMBDA:
                if peek(key):
                    print("heree")
                    gram[key].remove(constant.LAMBDA)
    print ("final print: ", gram )
    return gram


def peek(nonterminal):
    xd = []
    if nonterminal not in xd:
        xd.append(nonterminal)
        return True
    return False


def copy_grammar(grammar):
    gramm = dict()
    for nonterm, rule in grammar.items():
        gramm[nonterm] = rule.copy()
    return gramm




def normalizeToGreibach(grammar):

    print("Transform indirect left recursion to direct left recursion")
    checkForIndirectLeftRecursion(grammar)
    print(grammar)
    directLeftRecursionKeys = checkForDirectLeftRecursion(grammar)
    print("Direct Left Recursion NonTerminals =", list(set(directLeftRecursionKeys)), "Remove ->")
    removeDirectLeftRecursion(grammar, list(set(directLeftRecursionKeys)))
    print(grammar)
    print("Replace first NonTerminal with productions that have first char a terminal ->")
    replaceNTtoT(grammar)
    print(grammar)


def checkForDirectLeftRecursion(grammar):
    keys = list()
    for key in grammar:
        for production in grammar[key]:
            if production[0] == key:
                keys.append(key)
    return keys


def checkProductionHead(grammar, key, head, prevkey):

    if head.islower():
        return
    if key == head:
        return prevkey
    for production in grammar[head]:
        if production[0].isupper():
            if production[0] == head:
                return
            if production[0] == prevkey == key:
                return head
            elif production[0] == prevkey:
                return
            temp = checkProductionHead(grammar, key, production[0], head)
            if temp:
                return temp





def checkForIndirectLeftRecursion(grammar):

    for key in grammar:
        for production in grammar[key]:
            if production[0].isupper():
                temp = checkProductionHead(grammar, key, production[0],key)
                if temp and temp != key:
                    newlist = list()
                    for prod in grammar[temp]:#replace with all productions
                        newlist.append(prod+production[1:])
                    grammar[key].extend(newlist)
                    if grammar[key].__contains__(production):
                        grammar[key].remove(production)




def removeDirectLeftRecursion(grammar,keys):

    alphabet = list(set(string.ascii_uppercase) - set(grammar.keys()))
    alphabet.sort(reverse=True)

    for key in keys:
        alphas = list()
        betas = list()
        replaceKey = alphabet[0]
        newProductions = (list(),list())
        productions = grammar[key]
        for production in productions:
            if production[0] == key:#alphas
                newProductions[0].extend((production[1:], production[1:] + replaceKey))
            else:#betas
                newProductions[1].extend((production, production+replaceKey))

        grammar[replaceKey] = newProductions[0]
        grammar[key] = newProductions[1]
        alphabet.pop(0)


def replaceNTtoT(grammar):
    flag = True
    while flag:
        flag = False
        for key in grammar:
            newList = list()
            for production in grammar[key]:
                if production[0].isupper():
                    if all(i[0].islower() for i in grammar[production[0]]):
                        for innerProd in grammar[production[0]]:
                            if innerProd.islower():
                                changed = production.replace(production[0],innerProd, 1)
                                newList.append(changed)
                                flag = True
                            elif innerProd[0].islower():
                                newList.append(innerProd+production[1:])
                                flag = True
                    else:
                        newList.append(production)

                else:
                    newList.append(production)
            grammar[key] = newList
        print(grammar)




def normalizeToChomsky(grammar):
    dictionaryOfReplaces = dict()
    alphabet = list(set(string.ascii_uppercase) - set(grammar.keys()))
    alphabet.sort(reverse=True)
    replaceTerminals(grammar, dictionaryOfReplaces, alphabet)
    print("Chomsky Normalization Step 1: Replace terminals with NonTerminals ->\n", grammar)
    divideNonTerminals(grammar, dictionaryOfReplaces, alphabet)
    print("Chomsky Normalization Step 2: Replace chunks with NonTerminals ->\n", grammar)
    newDict = dict()
    for key in dictionaryOfReplaces:
        newDict[dictionaryOfReplaces[key]] = [key]
    grammar.update(newDict)

    print (grammar)
'''
        "S" : ["aaB", "abAF", "aaSE", "F"],
        "A" : ["aA"],
        "B" :["ab", "b", "E"],
        "C": ["aD"],
        "D" : ["abE", "F"],
        "E" : ["λ", "ab"],
        "F": ["λ"]
'''

def replaceTerminals(grammar, dictionaryOfReplaces, alphabet):
    for key in grammar:
        newList = list()
        for production in grammar[key]:
            if len(production) > 1 and not production.isupper():
                changed = production
                for char in production:
                    if char.islower() and char not in dictionaryOfReplaces:
                        dictionaryOfReplaces[char] = alphabet[-1]
                        changed = changed.replace(char, alphabet[-1])
                        alphabet.pop()
                    elif char.islower():
                        changed = changed.replace(char, dictionaryOfReplaces[char])
                newList.append(changed)
            else:
                newList.append(production)
        grammar[key] = newList


def divideProduction(grammar, production, dictionaryOfReplaces, alphabet):
    changed = production
    chunks = [production[i:i + 2] for i in range(0, len(production), 2)]
    if len(chunks) <= 4:
        for prod in chunks:
            if prod not in dictionaryOfReplaces:
                if len(prod) % 2 == 0:
                    temp = alphabet[-1]
                    dictionaryOfReplaces[prod] = temp
                    changed = changed.replace(prod, temp)
                    alphabet.pop()
            elif prod in dictionaryOfReplaces:
                changed = changed.replace(prod, dictionaryOfReplaces[prod])
    return changed


def divideNonTerminals(grammar, dictionaryOfReplaces, alphabet):
    for key in grammar:
        newList = list()
        for production in grammar[key]:
            if len(production) in [1, 2]:
                newList.append(production)
            else:
                newList.append(divideProduction(grammar, production, dictionaryOfReplaces, alphabet))
        grammar[key] = newList



def remove_unit_productions(grammar):
    unitProductions = getUnitProductions(grammar)
    print("Unit Productions = ", unitProductions)
    for key in unitProductions:
        for production in unitProductions[key]:
            grammar[key].extend(set(grammar[production]) - set(grammar[key]))

# S -> Aa | B
# A -> b | B
# B -> A | a
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

    # remove unit productions
    for key in unitProductions:
        for production in unitProductions[key]:
            if grammar[key].__contains__(production):
                grammar[key].remove(production)


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

    # if a NonTerminal has as productions 2 NonTerminals that can be productive or not productive
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

def removeNonProductive(grammar):
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

'''
        "S" : ["aaB", "abA", "aaSE", "X"],
        "A" : ["aA"],
        "B" :["ab", "b", "E"],
        "C": ["aD"],
        "D" : ["abE"],
        "E" : [ "ab"]

        X : []


'''

if __name__ == "__main__":
    convertToGNF({
        "S" : ["abS", "abA", "abB"],
        "A" : ["cd", "λ"],
        "B" :["aB"],
        "C": ["dc"], 
    })

    print("------------------------")
    convertToGNF({
        "S" : ["aaB", "abAF", "aaSE", "F"],
        "A" : ["aA"],
        "B" :["ab", "b", "E"],
        "C": ["aD"],
        "D" : ["abE", "F"],
        "E" : ["λ", "ab"],
        "F": ["λ"]
    })

    print("------------------------")
    convertToGNF({
        "S" : ["aaB", "abAF", "aaSE", "F", "X"],
        "A" : ["aA"],
        "B" :["ab", "b", "E"],
        "C": ["aD"],
        "D" : ["abE", "F"],
        "E" : ["λ", "ab"],
        "F": ["λ"],
        "X":["F"]
    })    
    print("---------------------")
    convertToGNF({
        "S" : ["Aa", "B"],
        "A" : ["b", "B"],
        "B" :["A", "a"]
    })
    print("---------------------")
    convertToGNF({
        "S" : ["XA", "BB"],
        "A" : ["a"],
        "B" :["b", "SB"],
        "X":["b"]
    })  
    print("---------------------")
    convertToGNF({
        "S" : ["aSbb", "a"]
    })  
# S → XA|BB 
# B → b|SB 
# X → b 
# A → a
    

# S -> Aa | B
# A -> b | B
# B -> A | a