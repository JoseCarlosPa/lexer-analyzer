"""
---------------------------------------------------------------------------------------------------------
*
*       Jose Carlos Pacheco Sanchez - A01702828
*       Compiladores - Feb-Jun 2022 - Qro
*       Name: LL Table generator
*       Based on: https://github.com/Manchas2k4/compilers/tree/master/examples/lexical_analyzer
*       File: Functions and methods files part 3
*
---------------------------------------------------------------------------------------------------------
"""


class Color:
    OKBLUE = '\033[94m'
    GREEN = '\033[0;32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


# Check if word is in array
def is_in_array(word, array):
    already = True if word in array else False
    return already


# Remove an object from an array
def del_from_terminals(w_str, array):
    if w_str in array:
        array.remove(w_str)
    return array


# Print the arrays
def output_array(array, is_terminal):
    string = 'Terminales: ' if is_terminal else 'No Terminales: '
    for sym in array:
        string += sym + ', '
    print(string)


# Defines the non-terminals and terminals from a line
def next_line_read(line, terminal, non_terminals):
    r_side = False
    pile = []
    for word in line.split():
        pile.append(word)
        if word == '->':
            r_side = True
            pile.pop()
            new_non_terminal = pile.pop()
            if not is_in_array(new_non_terminal, non_terminals):
                non_terminals.append(new_non_terminal)
            terminal = del_from_terminals(new_non_terminal, terminal)
        elif r_side and word != "'":
            if not is_in_array(word, non_terminals) and not is_in_array(word, terminal):
                terminal.append(word)
    return terminal, non_terminals


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
    for dictionary in dictionaries:
        if dictionary["ruleKey"] == key:
            return dictionary
    dictionaries.append(empty)
    return empty


# Get the key given a rule and a value
def get_key(rules, key, value):
    for rule in rules:
        if rule["ruleKey"] == key:
            return rule[str(value)]


# Check for the first rule of epsilon  X -> A is a terminal
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
        if element != '->': # Check for roght side of the cchains
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
def get_first_of(rules, element, terminals):
    if is_in_array(element, terminals):
        return element
    elif element == "'":
        return []
    else:
        return get_key(rules, element, "FIRST")


# Check for the first if its terminal
def is_first_terminal(line, rules, terminals):
    has_epsilon = True
    for rule in rules:
        if len(rule["FIRST"]) > 0:
            for t in rule["FIRST"]:
                if not is_in_array(t, terminals) and t != '€':
                    rule['FIRST'] = list(set(rule['FIRST']) | set(is_first_non_terminal(t, rules)))
                    rule['FIRST'].remove(t)
        # Check the array length
        if len(rule["FIRST"]) <= 0:
            for nt in rule["ntFIRSTS"]:
                if has_epsilon:
                    rule['FIRST'] = list(set(rule['FIRST']) | set(is_first_non_terminal(nt, rules)))
                    has_epsilon = get_key(rules, nt, "hasEpsilon")
                else:
                    return


# Get the follow on the terminals
def get_follow(rule, rules, terminals):
    rule_ley = rule["ruleKey"]
    for allRule in rules:
        for number_rules in allRule["rules"]:
            if is_in_array(rule_ley, number_rules["rule"]):
                index = number_rules["rule"].index(rule_ley) + 1
                if index == len(number_rules["rule"]):
                    follow = allRule["FOLLOW"]
                    rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(follow))
                elif index < len(number_rules["rule"]):
                    next_ln = get_first_of(rules, number_rules["rule"][index], terminals)
                    if is_in_array("€", next_ln):
                        follow = list(set(rule['FOLLOW']) | set(next_ln))
                        next_ln = list(set(allRule["FOLLOW"]) | set(follow))
                        rule["FOLLOW"] = next_ln
                        # Get the Epsilons
                        if '€' in rule["FOLLOW"]:
                            rule["FOLLOW"].remove('€')
                    else:
                        rule["FOLLOW"] = list(set(rule['FOLLOW']) | set(next_ln))
                        if '€' in rule["FOLLOW"]:
                            rule["FOLLOW"].remove('€')


# Check if the grammatic has LL1
def get_grammatical_ll1(rule, rules, terminals):
    firsts = []
    for r in rule["rules"]:
        first = r["rule"][0]
        right_first = []
        right_first = get_first_of(rules, first, terminals)
        for i in right_first:
            if not is_in_array(i, firsts):
                firsts.append(i)
            else:
                return False
    return True


# Function to print the html table with al the rules and parsers
def print_html(r, rules, non_terminals):
    row = {
        "rule": [],
        "nt": [],
        "t": []
    }
    for first in r["FIRST"]:
        not_found = True
        for rule_key in r["rules"]:
            for charInKeyRule in rule_key["rule"]:
                if charInKeyRule == first:
                    row['nt'].append(r["ruleKey"])
                    row['t'].append(first)
                    not_append = r["ruleKey"] + ' -> ' + ''.join(rule_key["rule"])
                    row['rule'].append(not_append)
                    not_found = False

        if not_found: # Sames as below but with no terminals rules
            for rule_key in r["rules"]:
                for charInKeyRule in rule_key["rule"]:
                    if is_in_array(charInKeyRule, non_terminals):
                        for rule in rules:
                            if rule["ruleKey"] == charInKeyRule:
                                for nonTerminalRules in rule["rules"]:
                                    for charInRule in nonTerminalRules["rule"]:
                                        if charInRule == first:
                                            row['nt'].append(r["ruleKey"])
                                            row['t'].append(first)
                                            not_append = r["ruleKey"] + ' -> ' + ''.join(rule_key["rule"])
                                            row['rule'].append(not_append)
                                            not_found = False
        if not_found: # Sames as up but with terminal and founders
            for rule_key in r["rules"]:
                for charInKeyRule in rule_key["rule"]:
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
                                                                not_append = r["ruleKey"] + ' -> ' + ''.join(
                                                                    rule_key["rule"])
                                                                row['rule'].append(not_append)
                                                                not_found = False
    return row
