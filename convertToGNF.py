import string
import Utils.constants as constant


def convertToGNF(productions):
    print ("Removing Lamda")
    checkEmpty2(productions)
    #checkEmpty(productions, "S")
    print (productions)

    # deleteEmptySymbols(productions)
    # print(productions)

    remove(grammar=productions)
    print(productions)

    print("removing unit productions")
    removeRenaiming(productions)
    print(productions)


    #addStartingState(productions)
    print ("Removing Non accessible")
    productions = removeNonAccesible(productions)
    print(productions)

    print ("Removing Non productive")
    productions = removeNonProductive(productions)
    print (productions)

    normalizeToChomsky(productions)
    normalizeToGreibach(productions)

    #addStartingState(productions)
    print ("Removing Non accessible")
    productions = removeNonAccesible(productions)
    print(productions)

    print ("Removing Non productive")
    productions = removeNonProductive(productions)
    print (productions) 

    return productions   

    
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



def removeRenaiming(grammar):
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

def removeNonAccesible(productions):
    accesible = ["S"]
    accesible = checkAccesible(productions, "S", accesible)
    
    nonTerminals = set(productions.keys())
    nonAccesible = set(nonTerminals) - set(accesible)
    print("Non Accesible = ", nonAccesible)
    for key in nonAccesible:
        productions.pop(key)
    
    return productions

# Function to that adds a starting state - NE3MELHA BA3DEEN
def addStartingState(productions, S):

    to_add_S0 = False
    for i in range(len(productions)):
        if productions[i][0] == S:
            to_add_S0 = True
    if to_add_S0:
        productions.append(('S0', S))
        S = 'S0'

    productions = [pair for pair in productions if pair[1] != 'epsilon']

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

def remove(grammar):
    deleted = True

    while deleted:
        deleted = False
        toBePopped = []
        for key in grammar:
            if len(grammar[key]) == 0:
                toBePopped.append(key)
            for  i, production in enumerate(grammar[key]):
                if len(production) == 0:
                    grammar[key].remove(production)
                    deleted = True
                for char in production:
                    if char.isupper() and char not in grammar:
                        grammar[key][i] = production.replace(char,"")
                        deleted = True
                if len(grammar[key][i]) == 0:
                    grammar[key].remove(grammar[key][i])
        
        for p in toBePopped:
            grammar.pop(p)
            deleted = True
vis = set()

def checkEmpty2(grammar):
    for key in grammar:
        for production in grammar[key]:
            if production == constant.LAMBDA:
                grammar[key].remove(production)

def checkEmpty(grammar, key):

    #vis.add(key)
    
    for i, production in enumerate(grammar[key]):
        if production == constant.LAMBDA:
            grammar[key].remove(production)
            if len(grammar[key]) == 0:
                return True
        else:
            for char in production:
                if char.isupper() and char != key:# and char not in vis:

                    if checkEmpty(grammar, char) == True:
                        grammar[key][i] = production.replace(char,"")
            if len(grammar[key][i]) == 0:
                grammar[key].remove(grammar[key][i])
    
    if (len(grammar[key]) == 0):
        return True
    
    return False

def deleteEmptySymbols(grammar):
    toBeDeleted = []
    for symbol in grammar:
        if len(grammar[symbol]) == 0:
            toBeDeleted.append(symbol)
    
    for s in toBeDeleted:
        grammar.pop(s)

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