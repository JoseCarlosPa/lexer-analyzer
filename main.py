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

while True:

    file = input("Enter the file name: \n")
    f = open(file, "r")

    n = f.readline().split()
    n_productions = int(n[0])

    n_chains = int(n[1])

    print("\nNumber of Productions:", n_productions)
    
    terminals = []
    non_terminals = []
    
    for i in range(n_productions):
        line = f.readline()
        next_line_read(line, terminals, non_terminals)

    get_array(terminals, True)
    get_array(non_terminals, False)
    
    f.seek(0)
    line = f.readline()
    rules = []
    for i in range(n_productions):
        line = f.readline()
        get_if_first_terminal(line, terminals, non_terminals, rules, i)

    f.seek(0)
    line = f.readline()
    for i in range(n_productions):
        line = f.readline()
        is_first_terminal(line, rules,terminals)
    
    rules[0]["FOLLOW"].append('$')
    for rule in rules:
        get_follow(rule, rules,terminals)
    
    for rule in rules:
        print("ruleKey: ", rule["ruleKey"])
        print("FIRST: ", rule["FIRST"])
        print("FOLLOW: ", rule["FOLLOW"])
        print("rules: ", rule["rules"])
        print("\n")

    LL = True
    for rule in rules:
        LL1 = get_grammatical_ll1(rule, rules,terminals)
        if not LL1:
            LL = False

    if LL:
        print("Cumple con la primera regla de la gramatica LL(1)")
    else:
        print("No cumple con la primera regla de la gramatica LL(1)")

    header = '<table border="1" >\n\t<tr>\n\t\t<th>Non-terminals</th>'
    for terminal in terminals:
        header += '\n\t\t<th>'
        header += terminal
        header += '</th>'
    
    header += '\n\t\t<th>$</th>'

    for rule in rules:
        header += '\n\t<tr>\n\t\t<td>' + rule["ruleKey"] + '</td>'
        tab = print_html(rule, rules,non_terminals)
        for t in terminals:
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

    again = str(input("\nQuit? \ny - YES \nn - NO\n"))
