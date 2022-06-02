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
from datetime import date

while True:
    try:
        filename = input("Ingresa el nombre del archivo: \n")
        file = open(filename, "r")

        n = file.readline().split()
        n_productions = int(n[0])

        n_chains = int(n[1])

        terminals = []
        non_terminals = []

        for i in range(n_productions):
            line = file.readline()
            next_line_read(line, terminals, non_terminals)

        print("Numero de producciones:", n_productions)
        print('\n**********************************')
        output_array(terminals, True)
        output_array(non_terminals, False)
        print('**********************************\n')

        file.seek(0)
        line = file.readline()
        rules = []
        for i in range(n_productions):
            line = file.readline()
            get_if_first_terminal(line, terminals, non_terminals, rules, i)

        file.seek(0)
        line = file.readline()
        for i in range(n_productions):
            line = file.readline()
            is_first_terminal(line, rules, terminals)

        rules[0]["FOLLOW"].append('$')
        for rule in rules:
            get_follow(rule, rules, terminals)

        for rule in rules:
            print(str(rule["ruleKey"]) + " => FIRST = {" + str(sorted(rule["FIRST"]))[1:-1] + "} , FOLLOW = {" + str(
                rule["FOLLOW"])[1:-1] + "}")
            print("\n")

        LL = True
        for rule in rules:
            LL1 = get_grammatical_ll1(rule, rules, terminals)
            if not LL1:
                LL = False

        if LL:
            print(Color.GREEN + "Cumple con la primera regla de la gramatica LL(1)" +  Color.ENDC)
            print(Color.WARNING + "La tabla la podras ver en" + Color.ENDC + Color.OKBLUE + "/test_cases/fecha_de_hoy-Table.html" + Color.ENDC)
        else:
            print(Color.FAIL + "No cumple con la primera regla de la gramatica LL(1)" + Color.ENDC)
            quit()
        header = '<table border="1" >\n\t<tr>\n\t\t<th>Non-terminals</th>'
        for terminal in terminals:
            header += '\n\t\t<th>'
            header += terminal
            header += '</th>'

        header += '\n\t\t<th>$</th>'

        for rule in rules:
            header += '\n\t<tr>\n\t\t<td>' + rule["ruleKey"] + '</td>'
            tab = print_html(rule, rules, non_terminals)
            for t in terminals:
                notFound = True
                for terInTable in tab['t']:
                    if t == terInTable:
                        n = tab['t'].index(t)
                        header += '\n\t\t<td style="min-width:50px">' + tab["rule"][n] + '</td>'
                        notFound = False
                if notFound:
                    header += '\n\t\t<td style="min-width:50px"> </td>'
            header += '\n\t</tr>'

        header += '\n\t</tr>\n</table>'

        count = 1
        for rule in rules:
            header += '\n<p><strong>Input#:' + str(count) + '</strong>' + str(rule["rules"]) + '</p>'
            count = count + 1

        today = date.today()

        with open('test_cases/Table-' + str(today) + '.html', 'w') as file:
            file.write(header)

        file.close()

    except OSError as err:
        print(Color.FAIL + "!!Mmm creo no existe ese archivo o directorio, vuelve a intentar: {0}".format(
            err) + Color.ENDC)

    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

    again = str(input("\nIntentar con nuevo archivo? \ny - YES \nn - NO\n"))
    if again == 'n':
        quit()
