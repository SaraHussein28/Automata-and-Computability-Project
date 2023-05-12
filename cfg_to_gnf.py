import string
import Utils.constants as constant
import simplify_cfg


def convertToGNF(grammar):

    simplify_cfg.simplify_grammar(grammar=grammar)
    print("Simplified Grammar: \n", grammar)

    normalizeToChomsky(grammar)
    normalizeToGreibach(grammar)

    print ("Removing Non accessible")
    grammar = simplify_cfg.remove_non_accessible(grammar)
    print(grammar)

    print ("Removing Non productive")
    grammar = simplify_cfg.remove_non_productive(grammar)
    print (grammar) 

    return grammar   


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
