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


while True:
    menu()
    try:
        select = int(input('¿Que deseas hacer?:'))

        if select == 1:
            read_process()

        if select == 2:
            os.chdir('./test_cases')
            os.system('ls')
            print(Color.OKBLUE + "Selecciona un test:" + Color.ENDC)
            read_process()
            os.chdir('..')

        if select == 3:
            exit()

    except ValueError:
        print(Color.WARNING + "Creo ingresaste algo que no es un numero, vuelve a intentar" + Color.ENDC)
