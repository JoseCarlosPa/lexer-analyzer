class Color:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def menu():
    print('-----Menu-----:')
    print('1.- Seleccionar una archivo:')
    print('2.- Usar pruebas de "test_cases":')
    print('3.- Salir')


def is_array(str, array):
    return True if str in array else False  # Check if a given string is on the array


def read_line(line, term, no_term):
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
            term = rm_from_terminals(new_non_terminal, term)
        elif r_side and str != "'":  # Not counting case for '
            if not is_array(str, no_term) and not is_array(str, term):
                term.append(str)
    return term, no_term


def rm_from_terminals(str, array):
    if str in array:
        array.remove(str)
    return array


def output_array(array, terminal):
    string = 'Terminal: ' if terminal else 'Non terminal: '
    for sym in array:
        string += sym + ', '
    print(string)


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

