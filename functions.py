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
def is_in_array(word, array):
    already = True if word in array else False
    return already


# Remove an object from an array
def del_from_terminals(word, array):
    if word in array:
        array.remove(word)
    return array


# Print the arrays
def get_array(array, is_terminal):
    string = 'Terminales: ' if is_terminal else 'No Terminales: '
    for sym in array:
        string += sym + ', '
    print(string)


# Defines the non-terminals and terminals from a line
def next_line_read(line, t, nt):
    stack = []
    right = False
    # First word will always be a non-terminal expresion
    for word in line.split():
        stack.append(word)
        if word == '->':
            right = True
            stack.pop()
            newNonTerminal = stack.pop()
            if not is_in_array(newNonTerminal, nt):
                nt.append(newNonTerminal)
            t = del_from_terminals(newNonTerminal, t)
        elif right and word != "'":
            if not is_in_array(word, nt) and not is_in_array(word, t):
                t.append(word);
    return t, nt;


# Check if the non-terminal key is already in dictionary, if not returns a new entry with the key on it
def set_key(dictionaries, key):
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


# Get the key given a rule and a value
def get_key(rules, key, value):
    for rule in rules:
        if rule["ruleKey"] == key:
            return rule[str(value)]


# Check for the first rule of epsilon  X -> a is a terminal
def get_if_first_terminal(line, terminals, non_terminals, rules, index):

    line = line.split()
    rule = set_key(rules, line[0])
    del line[:2]
    first = True
    body = {
        "index": index,
        "rule": line,
    }
    rule["rules"].append(body)
    for element in line:
        if element != '->':
            if first:
                if is_in_array(element, terminals):
                    if not is_in_array(element, rule["FIRST"]):
                        rule["FIRST"].append(element)
                        return rule
                elif element == "'":
                    rule["hasEpsilon"] = True
                    rule["FIRST"].append('€')
                    return
                else:
                    if not is_in_array(element, rule["FIRST"]):
                        rule["FIRST"].append(element)
                        return rule
            elif element == "'":
                rule["hasEpsilon"] = True
            else:
                if not is_in_array(element, rule["ntFIRSTS"]):
                    rule["ntFIRSTS"].append(element)
            first = False

    return rule


# Check for the first of nt symbols
def is_first_non_terminal(nt, rules):
    for rule in rules:
        if rule["ruleKey"] == nt:
            if len(rule["FIRST"]) > 0:
                return rule["FIRST"]
            elif len(rule["ntFIRSTS"]) > 0:
                for ntF in rule["ntFIRSTS"]:
                        return is_first_non_terminal(ntF, rules)


# Get the first of rules and return with terminals
def get_first_of(rules, element,Terminals):
    if is_in_array(element, Terminals):
        return element
    elif element == "'":
        return []
    else:
        return get_key(rules, element, "FIRST")


# Check for the first if its terminal
def is_first_terminal(line, rules,Terminals):
    hasEpsilon = True
    for rule in rules:
        if len(rule["FIRST"]) > 0:
            for t in rule["FIRST"]:
                    if not is_in_array(t, Terminals) and t != '€':
                        rule['FIRST'] = list(set(rule['FIRST']) | set(is_first_non_terminal(t, rules)))
                        rule['FIRST'].remove(t)
        if len(rule["FIRST"]) <= 0:
            for nt in rule["ntFIRSTS"]:
                    if hasEpsilon:
                        rule['FIRST'] = list(set(rule['FIRST']) | set(is_first_non_terminal(nt, rules)))
                        hasEpsilon = get_key(rules, nt, "hasEpsilon")
                    else:
                         return


# Get the follow on the terminals
def get_follow(rule, rules,Terminals):
    ruleKey = rule["ruleKey"]
    for allRule in rules:
        for nRule in allRule["rules"]:
            if is_in_array(ruleKey, nRule["rule"]):
                index = nRule["rule"].index(ruleKey) + 1
                if index == len(nRule["rule"]) :
                    follow = allRule["FOLLOW"]
                    rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(follow))
                elif index < len(nRule["rule"]) :
                    firstNext = get_first_of(rules, nRule["rule"][index],Terminals)
                    if is_in_array("€", firstNext):
                        follow = list(set(rule['FOLLOW']) | set(firstNext))
                        firstNext =  list(set(allRule["FOLLOW"]) | set(follow))
                        rule["FOLLOW"] = firstNext
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')
                    else:
                        rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(firstNext))
                        if '€' in rule["FOLLOW"]: rule["FOLLOW"].remove('€')


# Check if the grammatic has LL1
def get_grammatical_ll1(rule, rules,Terminals):
    firsts = []
    for r in rule["rules"]:
        first = r["rule"][0]
        rfirsts = []
        rfirsts = get_first_of(rules, first,Terminals)
        for e in rfirsts:
            if not is_in_array(e, firsts):
                firsts.append(e)
            else:
                return False
    return True


def print_html(r, rules,non_terminals):
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
                    if(is_in_array(charInKeyRule, non_terminals)):
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
                    if is_in_array(charInKeyRule, non_terminals):
                        for nonTerminal in rules:
                            if nonTerminal["ruleKey"] == charInKeyRule:
                                for nonTerminalRules in nonTerminal["rules"]:
                                    for ruleInNonTerminal in nonTerminalRules["rule"]:
                                        if is_in_array(ruleInNonTerminal, non_terminals):
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

