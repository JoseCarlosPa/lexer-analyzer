"""
---------------------------------------------------------------------------------------------------------
*
*       Jose Carlos Pacheco Sanchez - A01702828
*       Compiladores - Feb-Jun 2022 - Qro
*       Name: Analizador Lexico
*       Based on: https://github.com/Manchas2k4/compilers/tree/master/examples/lexical_analyzer
*
---------------------------------------------------------------------------------------------------------
"""
from functions import *
import os


# Check if the non terminal key is already in dictionary, if not returns a new entry with the key on it
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


#
def getValueForKey(rules, key, value):
    for rule in rules:
        if rule["ruleKey"] == key:
            return rule[str(value)]

# Check for the first rule of epsilon  X -> a, a is a terminal
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
        if element != '->':
            if (first):
                if is_array(element, terminals):
                    if not is_array(element, rule["FIRST"]):
                        rule["FIRST"].append(element)
                        return rule
                else:
                    if not is_array(element, rule["FIRST"]):
                        rule["FIRST"].append(element)
                        return rule
            elif element == "'":
                rule["hasEpsilon"] = True
            else:
                if not is_array(element, rule["ntFIRSTS"]):
                    rule["ntFIRSTS"].append(element)
            first = False

    return rule


# Check for the first of nt symbols
def firstNTR(nt, rules):
    for rule in rules:
        if rule["ruleKey"] == nt:
            if len(rule["FIRST"]) > 0:
                return rule["FIRST"]
            elif len(rule["ntFIRSTS"]) > 0:
                for ntF in rule["ntFIRSTS"]:
                    return firstNTR(ntF, rules)


def firstCase2(line, rules):
    hasEpsilon = True
    for rule in rules:
        if len(rule["FIRST"]) > 0:
            for t in rule["FIRST"]:
                if not is_array(t, Terminals):
                    rule['FIRST'] = list(set(rule['FIRST']) | set(firstNTR(t, rules)))
                    rule['FIRST'].remove(t)
        if len(rule["FIRST"]) <= 0:
            for nt in rule["ntFIRSTS"]:
                if (hasEpsilon):
                    rule['FIRST'] = list(set(rule['FIRST']) | set(firstNTR(nt, rules)))
                    hasEpsilon = getValueForKey(rules, nt, "hasEpsilon")
                else:
                    return

def getFirstOf(rules, element):
    if is_array(element, Terminals):
        return element
    elif element == "'":
        return []
    else:
        return getValueForKey(rules, element, "FIRST")

def follow(rule, rules):
    ruleKey = rule["ruleKey"]
    for allRule in rules:
        for nRule in allRule["rules"]:
            if is_array(ruleKey, nRule["rule"]):
                index = nRule["rule"].index(ruleKey) + 1
                if index == len(nRule["rule"]) :
                    follow = allRule["FOLLOW"]
                    rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(follow))
                elif index < len(nRule["rule"]) :
                    firstNext = getFirstOf(rules, nRule["rule"][index])
                    if is_array("€", firstNext):
                        follow = list(set(rule['FOLLOW']) | set(firstNext))
                        firstNext =  list(set(allRule["FOLLOW"]) | set(follow))
                        rule["FOLLOW"] = firstNext
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')
                    else:
                        rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(firstNext))
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')

while True:
    menu()
    try:
        select = int(input('¿Que deseas hacer?:'))

        if select == 1:
            read_process()

        if select == 2:
            filename = input("Ingresa el nombre del archivo:\n")
            f = open(filename, "r")
            nProductions = int(f.readline())

            Terminals = []
            NonTerminals = []

            for i in range(nProductions):
                line = f.readline()
                read_line(line, Terminals, NonTerminals)

            print("\n-------------------------")
            output_array(Terminals, True)
            output_array(NonTerminals, False)
            print("-------------------------\n")

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
                print(str(rule["ruleKey"]) + " => FIRST = {" + str(sorted(rule["FIRST"]))[1:-1] + "} , FOLLOW = {" + str(rule["FOLLOW"])[1:-1] + "}")

                print("\n")

            f.close()

            isLL1 = True
            for rule in rules:
                if (rule["hasEpsilon"]):
                    isLL1 = False
                    break
                for nt in rule["ntFIRSTS"]:
                    if (getValueForKey(rules, nt, "hasEpsilon")):
                        isLL1 = False
                        break
            if (isLL1):
                print("\nLL(1) YES")
            else:
                print("\nLL(1) NO")


        if select == 3:
            exit()

    except ValueError:
        print(Color.WARNING + "Creo ingresaste algo que no es un numero, vuelve a intentar" + Color.ENDC)