class Color:
    OKBLUE = '\033[94m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'


def menu():
    print('-----Menu-----:')
    print('1.- Seleccionar una archivo:')
    print('2.- Correr pruebas de "test_cases":')
    print('3.- Salir')


def is_array(word, array):
    already = True if word in array else False
    return already


def rm_from_terminals(word, array):
    if word in array:
        array.remove(word)
    return array


def output_array(array, terminal):
    string = 'Terminal: ' if terminal else 'Non terminal: '
    for sym in array:
        string += sym + ', '
    print(string)


def lineRead(line, t, nt):
    stack = []
    right = False
    for word in line.split():
        stack.append(word)
        if word == '->':
            right = True
            stack.pop()
            new_non_terminal = stack.pop()
            if not is_array(new_non_terminal, nt):
                nt.append(new_non_terminal)
            t = rm_from_terminals(new_non_terminal, t)
        elif right and word != "'":
            if not is_array(word, nt) and not is_array(word, t):
                t.append(word)
    return t, nt


def read_process():
    try:
        filename = input("Ingresa el nombre o el path del archivo:\n")

        file = open(filename, "r")

        nProductions = int(file.readline())

        Terminals = []
        NonTerminals = []

        for i in range(nProductions):
            line = file.readline()
            t, nt = lineRead(line, Terminals, NonTerminals)

        print('\n')
        output_array(Terminals, True)
        output_array(NonTerminals, False)
        file.close()
        print('\n')
    except OSError as err:
        print(Color.FAIL + "!!Mmm creo no existe ese archivo o directorio, vuelve a intentar: {0}".format(
            err) + Color.ENDC)

    except ValueError:
        print("Could not convert data to an integer.")
    except BaseException as err:
        print(f"Unexpected {err=}, {type(err)=}")

