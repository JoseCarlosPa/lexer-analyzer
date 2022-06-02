"""
---------------------------------------------------------------------------------------------------------
*
*       Jose Carlos Pacheco Sanchez - A01702828
*       Compiladores - Feb-Jun 2022 - Qro
*       Name: Generador de is_first & is_follows
*       Based on: https://github.com/Manchas2k4/compilers/tree/master/examples/lexical_analyzer
*       File: Functions and methods files
*
---------------------------------------------------------------------------------------------------------
"""

# Check if word is in array
def isIn(word, array):
    already = True if word in array else False
    return already

#remove an object from an array
def removeFromTerminals(word, array):
    if(word in array):
        array.remove(word)
    return array

#Print the arrays
def printArray(array, isTerminal):
    string = 'Terminales: ' if isTerminal else 'No Terminales: '
    for sym in array:
        string += sym + ', '
    print(string)


# Defines the non-terminals and terminals from a line
def lineRead(line, t, nt):
    stack = []
    right = False
    # First word will always be a non-terminal expresion
    for word in line.split():
        stack.append(word)
        if (word == '->'):
            right = True
            stack.pop()
            newNonTerminal = stack.pop()
            if(not isIn(newNonTerminal, nt)):
                nt.append(newNonTerminal)
            t = removeFromTerminals(newNonTerminal, t)
        elif(right and word != "'"):
            if (not isIn(word, nt) and not isIn(word, t)):
                t.append(word);
    return t, nt;



#Check if the non terminal key is already in dictionary, if not returns a new entry with the key on it
def isAlreadyKey(dictionaries, key):
    empty = {
        "ruleKey": key,
        "rules": [],
        "FIRST": [],
        "FOLLOW": [],
        "ntFIRSTS": [],
        "hasEpsilon": False
    }
    for dic in dictionaries:
        if dic["ruleKey"] == key:
            return dic
    dictionaries.append(empty)
    return empty




def getValueForKey(rules, key, value):
    for rule in rules:
        if rule["ruleKey"] == key:
            return rule[str(value)]



#Check for the first rule of epsilon  X -> a, a is a terminal
def firstCase(line, terminals, nonTerminals, rules, index):

    line = line.split()
    rule = isAlreadyKey(rules, line[0])
    del line[:2]
    first = True
    body = {
        "index": index,
        "rule": line,
    }
    rule["rules"].append(body)
    for element in line:
        if (element != '->'):
            if (first):
                if(isIn(element, terminals)):
                    if(not isIn(element, rule["FIRST"])):
                        rule["FIRST"].append(element)
                        return rule
                elif (element == "'"):
                    rule["hasEpsilon"] = True
                    rule["FIRST"].append('€')
                    return
                else:
                    if(not isIn(element, rule["FIRST"])):
                        rule["FIRST"].append(element)
                        return rule
            elif (element == "'"):
                rule["hasEpsilon"] = True
            else:
                if(not isIn(element, rule["ntFIRSTS"])):
                    rule["ntFIRSTS"].append(element)
            first = False

    return rule


#Check for the first of nt symbols
def firstNTR(nt, rules):
    for rule in rules:
        if(rule["ruleKey"] == nt):
            if(len(rule["FIRST"]) > 0):
                return rule["FIRST"]
            elif(len(rule["ntFIRSTS"]) > 0):
                for ntF in rule["ntFIRSTS"]:
                        return firstNTR(ntF, rules)

def getFirstOf(rules, element,Terminals):
    if isIn(element, Terminals):
        return element
    elif element == "'":
        return []
    else:
        return getValueForKey(rules, element, "FIRST")