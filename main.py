"""
---------------------------------------------------------------------------------------------------------
*
*       Jose Carlos Pacheco Sanchez - A01702828
*       Compiladores - Feb-Jun 2022 - Qro
*       Name: Generador de is_first & is_follows
*       Based on: https://github.com/Manchas2k4/compilers/tree/master/examples/lexical_analyzer
*       File: main program file
*
---------------------------------------------------------------------------------------------------------
"""
from functions import *
import os

# Get the first of the line
def get_first(actions, element):
    if is_array(element, terminals):
        return element
    elif element == "'":
        return []
    else:
        return get_key_value(actions, element, "is_first")

# Set if if contains an epislon to apply second rule of LL1
def is_first_contains_epsilon(actions):
    contains_epsilon = True
    for action in actions:
        if len(action["is_first"]) > 0:
            for t in action["is_first"]:
                if not is_array(t, terminals):
                    action['is_first'] = list(set(action['is_first']) | set(not_terminal_is_first(t, actions)))
                    action['is_first'].remove(t)
        if len(action["is_first"]) <= 0:
            for not_terminal in action["not_first"]:
                if contains_epsilon:
                    action['is_first'] = list(set(action['is_first']) | set(not_terminal_is_first(not_terminal, actions)))
                    contains_epsilon = get_key_value(actions, not_terminal, "contains_epsilon")
                else:
                    return

# Define with recursion the follow of a non terminal
def is_follow(action, actions):
    rule_key = action["rule_key"]
    for allRule in actions:
        for nRule in allRule["rules"]:
            if is_array(rule_key, nRule["rule"]):
                index = nRule["rule"].index(rule_key) + 1
                if index == len(nRule["rule"]) :
                    is_follow = allRule["is_follow"]
                    action["is_follow"] = list(set(action['is_follow']) | set(is_follow))
                elif index < len(nRule["rule"]) :
                    is_firstNext = get_first(actions, nRule["rule"][index])
                    if is_array("€", is_firstNext):
                        is_follow = list(set(action['is_follow']) | set(is_firstNext))
                        is_firstNext =  list(set(allRule["is_follow"]) | set(is_follow))
                        action["is_follow"] = is_firstNext
                        if '€' in action["is_follow"]: action["is_follow"].remove('€')
                    else:
                        action["is_follow"] = list(set(action['is_follow']) | set(is_firstNext))
                        if '€' in action["is_follow"]: action["is_follow"].remove('€')
            return


# Main function and menu options
while True:
    menu()
    try:
        select = int(input('¿Que deseas hacer?:'))

        # Lexer analyzer
        if select == 1:
            read_process()

        # First And Follows
        if select == 2:
            try:
                filename = input("Ingresa el nombre del archivo:\n")
                file = open(filename, "r")
                number_of_productions = int(file.readline())

                terminals = []
                non_terminals = []
                is_ll_1 = True

                for i in range(number_of_productions):
                    content = file.readline()
                    read_line(content, terminals, non_terminals)

                print("\n----------LEXER---------------")
                output_array(terminals, True)
                output_array(non_terminals, False)
                print("------------------------------\n")

                file.seek(0)
                content = file.readline()
                actions = []

                for i in range(number_of_productions):
                    content = file.readline()
                    is_first_case( i,content, terminals, actions)

                file.seek(0)
                content = file.readline()

                for i in range(number_of_productions):
                    content = file.readline()
                    is_first_contains_epsilon(actions)

                actions[0]["is_follow"].append('$')

                for action in actions:
                    is_follow(action, actions)

                for action in actions:
                    print(str(action["rule_key"]) + " => FIRST = {" + str(sorted(action["is_first"]))[1:-1] + "} , FOLLOW = {" + str(action["is_follow"])[1:-1] + "}")
                    print("\n")

                file.close()

                for action in actions:
                    if action["contains_epsilon"]:
                        is_ll_1 = False
                        break
                    for nt in action["not_first"]:
                        if get_key_value(actions, nt, "contains_epsilon"):
                            is_ll_1 = False
                            break

                if is_ll_1:
                    print("\nLL(1) YES")
                else:
                    print("\nLL(1) NO")

            except OSError as err:
                print(Color.FAIL + "!!Mmm creo no existe ese archivo o directorio, vuelve a intentar: {0}".format(
                    err) + Color.ENDC)

            except ValueError:
                print("Could not convert data to an integer.")
            except BaseException as err:
                print(f"Unexpected {err=}, {type(err)=}")

        # Finish the program
        if select == 3:
            exit()

    except ValueError:
        print(Color.WARNING + "Creo ingresaste algo que no es un numero, vuelve a intentar" + Color.ENDC)