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

# Prining color class
class Color:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

# Menu for the user
def menu():
    print('-----Menu-----:')
    print('1.- LEXER')
    print('2.- FIRST & FOLLOWS')
    print('3.- Salir')

# Definition of the action rules
def rules_list(dictionaries, key):
    empty = {
        "rule_key": key,
        "rules": [],
        "is_first": [],
        "is_follow": [],
        "not_first": [],
        "contains_epsilon": False
    }
    for dic in dictionaries:
        if dic["rule_key"] == key:
            return dic
    dictionaries.append(empty)
    return empty


# Check if the string is in the array
def is_array(str, array):
    return True if str in array else False  # Check if a given string is on the array

# Read the next line of the file
def read_line(line, terminal, no_term):
    r_side = False
    pile = []
    for str in line.split():
        pile.append(str)
        if str == '->':  # Split operator for right and left ->
            r_side = True
            pile.pop()
            new_non_terminal = pile.pop()
            if not is_array(new_non_terminal, no_term):
                no_term.append(new_non_terminal)
            terminal = rm_from_terminals(new_non_terminal, terminal)
        elif r_side and str != "'":  # Not counting case for '
            if not is_array(str, no_term) and not is_array(str, terminal):
                terminal.append(str)
    return terminal, no_term


# Remove a string from the terminal array
def rm_from_terminals(str, array):
    if str in array:
        array.remove(str)
    return array

# Output the array
def output_array(array, terminal):
    string = 'Terminal: ' if terminal else 'Non terminal: '
    for sym in array:
        string += sym + ', '
    print(string)

# Function for the lexer analysis
def read_process():
    try:
        filename = input("Ingresa el nombre o el path del archivo:\n")

        file = open(filename, "r")

        product = int(file.readline())
        terminals = []
        non_terminals = []

        for _ in range(product):
            line = file.readline()
            read_line(line, terminals, non_terminals)

        print('\n')
        output_array(terminals, True)
        output_array(non_terminals, False)
        file.close()
        print('\n')
    except OSError as err:
        print(Color.FAIL + "!!Mmm creo no existe ese archivo o directorio, vuelve a intentar: {0}".format(
            err) + Color.ENDC)

    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")


def get_key_value(actions, key, value):
    for action in actions:
        if action["rule_key"] == key:
            return action[str(value)]

def is_first_case(index, content, terminals, actions):
    is_first = True
    content = content.split()
    action = rules_list(actions, content[0])
    del content[:2]
    body = {
        "index": index,
        "rule": content,
    }
    action["rules"].append(body)
    for element in content:
        if element != '->':
            if is_first:
                if is_array(element, terminals):
                    if not is_array(element, action["is_first"]):
                        action["is_first"].append(element)
                        return action
                else:
                    if not is_array(element, action["is_first"]):
                        action["is_first"].append(element)
                        return action
            elif element == "'":
                action["contains_epsilon"] = True
            else:
                if not is_array(element, action["not_first"]):
                    action["not_first"].append(element)
            is_first = False

    return action



def not_terminal_is_first(not_terminal, actions):
    for action in actions:
        if action["rule_key"] == not_terminal:
            if len(action["is_first"]) > 0:
                return action["is_first"]
            elif len(action["not_first"]) > 0:
                for ntF in action["not_first"]:
                    return not_terminal_is_first(ntF, actions)


