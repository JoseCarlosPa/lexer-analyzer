"""
---------------------------------------------------------------------------------------------------------
*
*       Jose Carlos Pacheco Sanchez - A01702828
*       Compiladores - Feb-Jun 2022 - Qro
*       Name: Generador de is_first & is_follows
*       Based on: https://github.com/Manchas2k4/compilers/tree/master/examples/lexical_analyzer
*       File: Main component part 3
*
---------------------------------------------------------------------------------------------------------
"""

from functions import *


def firstCase2(line, rules):
    hasEpsilon = True
    for rule in rules:
        if(len(rule["FIRST"]) > 0):
            for t in rule["FIRST"]:
                    if(not isIn(t, Terminals) and t != '€'):
                        rule['FIRST'] = list(set(rule['FIRST']) | set(firstNTR(t, rules)))
                        rule['FIRST'].remove(t)
        if(len(rule["FIRST"]) <= 0):
            for nt in rule["ntFIRSTS"]:
                    if(hasEpsilon):
                        rule['FIRST'] = list(set(rule['FIRST']) | set(firstNTR(nt, rules)))
                        hasEpsilon = getValueForKey(rules, nt, "hasEpsilon")
                    else:
                         return



def follow(rule, rules):
    ruleKey = rule["ruleKey"]
    for allRule in rules:
        for nRule in allRule["rules"]:
            if isIn(ruleKey, nRule["rule"]):
                index = nRule["rule"].index(ruleKey) + 1
                if index == len(nRule["rule"]) :
                    follow = allRule["FOLLOW"]
                    rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(follow))
                elif index < len(nRule["rule"]) :
                    firstNext = getFirstOf(rules, nRule["rule"][index],Terminals)
                    if isIn("€", firstNext):
                        follow = list(set(rule['FOLLOW']) | set(firstNext))
                        firstNext =  list(set(allRule["FOLLOW"]) | set(follow))
                        rule["FOLLOW"] = firstNext
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')
                    else:
                        rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(firstNext))
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')

def gramaticaLL1(rule, rules):
    firsts = []
    for r in rule["rules"]:
        first = r["rule"][0]
        rfirsts = []
        rfirsts = getFirstOf(rules, first,Terminals)
        for e in rfirsts:
            if (not isIn(e, firsts)):
                firsts.append(e)
            else:
                return False
    return True

def table(r, rules):
    row = {
        "rule": [],
        "nt": [],
        "t": []
    }
    for first in r["FIRST"]:
        notFound = True
        for keyRule in r["rules"]:
            for charInKeyRule in keyRule["rule"]:
                if charInKeyRule == first:
                    row['nt'].append(r["ruleKey"]) # r is the original ruleKey
                    row['t'].append(first) # is part of the firsts of r
                    ntAppend = r["ruleKey"] +' -> '+''.join(keyRule["rule"])
                    row['rule'].append(ntAppend)
                    notFound = False
        #the first is not contained directly in the rules of the the key r
        if notFound:
            for keyRule in r["rules"]:
                for charInKeyRule in keyRule["rule"]:
                    if(isIn(charInKeyRule, NonTerminals)):
                        for rule in rules:
                            if rule["ruleKey"] == charInKeyRule:
                                for nonTerminalRules in rule["rules"]:
                                    for charInRule in nonTerminalRules["rule"]:
                                        if charInRule == first:
                                            row['nt'].append(r["ruleKey"])
                                            row['t'].append(first)
                                            ntAppend = r["ruleKey"] +' -> '+''.join(keyRule["rule"])
                                            row['rule'].append(ntAppend)
                                            notFound = False
        if notFound:
            for keyRule in r["rules"]:
                for charInKeyRule in keyRule["rule"]:
                    if(isIn(charInKeyRule, NonTerminals)):
                        for nonTerminal in rules:
                            if(nonTerminal["ruleKey"] == charInKeyRule):
                                for nonTerminalRules in nonTerminal["rules"]:
                                    for ruleInNonTerminal in nonTerminalRules["rule"]:
                                        if(isIn(ruleInNonTerminal, NonTerminals)):
                                            for NT in rules:
                                                if NT["ruleKey"] == ruleInNonTerminal:
                                                    for NTRules in NT["rules"]:
                                                        for NTRule in NTRules["rule"]:
                                                            if NTRule == first:
                                                                row['nt'].append(r["ruleKey"])
                                                                row['t'].append(first)
                                                                ntAppend = r["ruleKey"] +' -> '+''.join(keyRule["rule"])
                                                                row['rule'].append(ntAppend)
                                                                notFound = False
    return row



exit = False
while exit == False:
    # Reading the name of the file
    filename = input("Enter file name\n")

    f = open(filename, "r")

    n = f.readline().split()
    nProductions = int(n[0])

    nCadenas = int(n[1])

    print("nProductions", nProductions)
    
    Terminals = []
    NonTerminals = []
    
    for i in range(nProductions):
        line = f.readline()
        lineRead(line, Terminals, NonTerminals)


    printArray(Terminals, True)
    printArray(NonTerminals, False)
    
    f.seek(0)
    line = f.readline()
    rules = []
    for i in range(nProductions):
        line = f.readline()
        firstCase(line, Terminals, NonTerminals, rules, i)

    f.seek(0)
    line = f.readline()
    for i in range(nProductions):
        line = f.readline()
        firstCase2(line, rules)
    

    rules[0]["FOLLOW"].append('$')
    for rule in rules:
        follow(rule, rules)
    
    for rule in rules:
        print("ruleKey: ", rule["ruleKey"])
        print("FIRST: ", rule["FIRST"])
        print("FOLLOW: ", rule["FOLLOW"])
        print("rules: ", rule["rules"])
        print("\n")

    LL = True
    for rule in rules:
        LL1 = gramaticaLL1(rule, rules) 
        if not LL1 :
            LL = False

    if LL:
        print("Cumple con la primera regla de la gramatica LL(1)")
    else:
        print("No cumple con la primera regla de la gramatica LL(1)")

    header = '<table border="1" >\n\t<tr>\n\t\t<th>Non-terminals</th>'
    for t in Terminals:
        header += '\n\t\t<th>'
        header += t
        header += '</th>'
    
    header += '\n\t\t<th>$</th>'


    for rule in rules:
        header += '\n\t<tr>\n\t\t<td>' + rule["ruleKey"] + '</td>'
        tab = table(rule, rules)
        for t in Terminals:
            notFound = True
            for terInTable in tab['t']:
                if t == terInTable:
                    n = tab['t'].index(t)
                    header += '\n\t\t<td>' + tab["rule"][n] + '</td>'
                    notFound = False
            if notFound:
                header += '\n\t\t<td> </td>'
        header += '\n\t</tr>'
    
    header += '\n\t</tr>\n</table>'

    with open('table.html', 'w') as f:
        f.write(header)

    f.close()

    res = str(input("\nQuit? \ny - YES \nn - NO\n"))
    exit = True if res == 'y' else False
