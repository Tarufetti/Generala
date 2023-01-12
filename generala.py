import random
from re import S

dado1 = '       \n|       |\n|   *   |\n|       |\n       '
dado2 = '       \n| *     |\n|       |\n|     * |\n       '
dado3 = '       \n|   *   |\n|   *   |\n|   *   |\n       '
dado4 = '       \n| *   * |\n|       |\n| *   * |\n       '
dado5 = '       \n| *   * |\n|   *   |\n| *   * |\n       '
dado6 = '       \n| *   * |\n| *   * |\n| *   * |\n       '
listadedados= ['nada', dado1, dado2, dado3, dado4, dado5, dado6]

jugador = {'uno':'','dos':'','tres':'','cuatro':'','cinco':'','seis':'','escalera':'','full':'','poker':'','generala':'','generala doble':''}
jugador1 = {'uno':'','dos':'','tres':'','cuatro':'','cinco':'','seis':'','escalera':'','full':'','poker':'','generala':'','generala doble':''}
jugador2 = {'uno':'','dos':'','tres':'','cuatro':'','cinco':'','seis':'','escalera':'','full':'','poker':'','generala':'','generala doble':''}
jugador3 = {'uno':'','dos':'','tres':'','cuatro':'','cinco':'','seis':'','escalera':'','full':'','poker':'','generala':'','generala doble':''}
jugador4 = {'uno':'','dos':'','tres':'','cuatro':'','cinco':'','seis':'','escalera':'','full':'','poker':'','generala':'','generala doble':''}

def tirada_dados(jugador):
    tirada = []
    tirada2 = []
    tirada3 = []

    print('Primer tiro...')
    input('arroje los dados...')
    for i in range (5):
        tirada.append(random.randint(1, 6))
    tirada = sorted(tirada)
    print(listadedados[tirada[0]],listadedados[tirada[1]],listadedados[tirada[2]],listadedados[tirada[3]],listadedados[tirada[4]])
    if tirada == [1,2,3,4,5] or tirada == [2,3,4,5,6]:
        print('Escalera servida')
        if jugador['escalera'] == '':
            finalizar_escalera = input('Desea anotar la escalera servida?: ').lower
            if finalizar_escalera == 'si':
                jugador = {'escalera':25}
                return jugador
        elif jugador['escalera'] == 0:
            print('Ya tiene escalera. Vuelva a tirar.')
    elif tirada[0] == tirada[1] and tirada[0] == tirada [2] and tirada[3] == tirada[4]:
        print('Full servido')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ').lower
            if finalizar_full == 'si':
                jugador = {'full':35}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada[0] == tirada[1] and tirada[2] == tirada [3] and tirada[3] == tirada[4]:
        print('Full servido')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ').lower
            if finalizar_full == 'si':
                jugador = {'full':35}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada[0] == tirada[3] or tirada[1] == tirada[4]:
        print('poker servido')
        if jugador['poker'] == '':
            finalizar_poker = input('Desea anotar el poker?: ').lower
            if finalizar_poker == 'si':
                jugador = {'poker':45}
                return jugador
        elif jugador['poker'] == 0:
            print('Ya tiene poker. Vuelva a tirar.')
    elif tirada[0] == tirada[4]:
        print('Generala servida. Ganaste el juego!')
        print('***** GANADOR *****')
        return
    
    eleccion_de_tiro = input('Presione 1 para elegir los dados que se quiere quedar, o 0 para terminar el turno: ')
    print('Segundo tiro...')

    if eleccion_de_tiro == '1':
        
        while True:
            dadoelegido = int(input('escriba el dado que desea conservar, o presione 0 para finalizar: '))
            if dadoelegido >= 1 and dadoelegido <= 6:
                tirada2.append(dadoelegido)
            elif dadoelegido == 0:
               break
    elif eleccion_de_tiro == '0':
        return jugador
    
    while len(tirada2) < 5:
        for j in range (5-len(tirada2)):
            tirada2.append(random.randint(1, 6))
    tirada2 = sorted(tirada2)
    print(listadedados[tirada2[0]],listadedados[tirada2[1]],listadedados[tirada2[2]],listadedados[tirada2[3]],listadedados[tirada2[4]])

    if tirada2 == [1,2,3,4,5] or tirada2 == [2,3,4,5,6]:
        print('Escalera')
        if jugador['escalera'] == '':
            finalizar_escalera = input('Desea anotar la escalera?: ')
            if finalizar_escalera == 'si':
                jugador['escalera'] = 20
                print(jugador)
        elif jugador['escalera'] == 0:
            print('Ya tiene escalera. Vuelva a tirar.')
    elif tirada2[0] == tirada2[1] and tirada2[0] == tirada2[2] and tirada2[3] == tirada2[4]:
        print('Full')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ')
            if finalizar_full == 'si':
                jugador = {'full':30}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada2[0] == tirada2[1] and tirada2[2] == tirada2[3] and tirada2[3] == tirada2[4]:
        print('Full')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ')
            if finalizar_full == 'si':
                jugador = {'full':30}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada2[0] == tirada2[3] or tirada2[1] == tirada2[4]:
        print('poker servido')
        if jugador['poker'] == '':
            finalizar_poker = input('Desea anotar el poker?: ')
            if finalizar_poker == 'si':
                jugador = {'poker':30}
                return jugador
        elif jugador['poker'] == 0:
            print('Ya tiene tachado poker. Vuelva a tirar.')
    elif tirada2[0] == tirada2[4]:
        print('generala')
        if jugador['generala'] == '':
            finalizar_generala = input('Desea anotar la generala?: ')
            if finalizar_generala == 'si':
                jugador = {'generala':50}
                return jugador
        elif jugador['generala'] == 0:
            print('Ya tiene tachada la generala. Vuelva a tirar.')
        elif jugador['generala'] == 50:
            print ('Generala doble!')
            if jugador['generala doble'] == '':
                finalizar_generaladoble = input('Desea anotar la generala doble?: ')
            if finalizar_generaladoble == 'si':
                jugador = {'generala doble':100}
                return jugador
        elif jugador['generala doble'] == 0:
            print('Ya tiene tachada la generala doble. Vuelva a tirar.')

    
    
    eleccion_de_tiro = input('Presione 1 para elegir los dados que se quiere quedar, 0 para terminar el turno o cualquier tecla para tirar TODOS los dados: ')
    
    if eleccion_de_tiro == '1':
        print('Ultimo tiro...')
        while True:
            dadoelegido = int(input('escriba el dado que desea conservar, o presione 0 para finalizar: '))
            if dadoelegido > 1 and dadoelegido <= 6:
                tirada3.append(dadoelegido)
            elif dadoelegido == 0:
               break
    elif eleccion_de_tiro == '0':
        return jugador
    
    while len(tirada3) < 5:
        for j in range (5-len(tirada3)):
            tirada3.append(random.randint(1, 6))
    tirada3 = sorted(tirada3)
    print(listadedados[tirada3[0]],listadedados[tirada3[1]],listadedados[tirada3[2]],listadedados[tirada3[3]],listadedados[tirada3[4]])
    if tirada3 == [1,2,3,4,5] or tirada3 == [2,3,4,5,6]:
        print('Escalera')
        if jugador['escalera'] == '':
            finalizar_escalera = input('Desea anotar la escalera?: ').lower
            if finalizar_escalera == 'si':
                jugador = {'escalera':20}
                return jugador
        elif jugador['escalera'] == 0:
            print('Ya tiene escalera. Vuelva a tirar.')
    elif tirada3[0] == tirada3[1] and tirada3[0] == tirada3[2] and tirada3[3] == tirada3[4]:
        print('Full')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ').lower
            if finalizar_full == 'si':
                jugador = {'full':30}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada3[0] == tirada3[1] and tirada3[2] == tirada3[3] and tirada3[3] == tirada3[4]:
        print('Full')
        if jugador['full'] == '':
            finalizar_full = input('Desea anotar el full?: ').lower
            if finalizar_full == 'si':
                jugador = {'full':30}
                return jugador
        elif jugador['full'] == 0:
            print('Ya tiene full. Vuelva a tirar.')
    elif tirada3[0] == tirada3[3] or tirada3[1] == tirada3[4]:
        print('poker ')
        if jugador['poker'] == '':
            finalizar_poker = input('Desea anotar el poker?: ').lower
            if finalizar_poker == 'si':
                jugador = {'poker':30}
                return jugador
        elif jugador['poker'] == 0:
            print('Ya tiene tachado poker. Vuelva a tirar.')
    elif tirada3[0] == tirada3[4]:
        print('generala')
        if jugador['generala'] == '':
            finalizar_generala = input('Desea anotar la generala?: ').lower
            if finalizar_generala == 'si':
                jugador = {'generala':50}
                return jugador
        elif jugador['generala'] == 0:
            print('Ya tiene tachada la generala. Vuelva a tirar.')
        elif jugador['generala'] == 50:
            print ('Generala doble!')
            if jugador['generala doble'] == '':
                finalizar_generaladoble = input('Desea anotar la generala doble?: ').lower
            if finalizar_generaladoble == 'si':
                jugador = {'generala doble':100}
                return jugador
        elif jugador['generala doble'] == 0:
            print('Ya tiene tachada la generala doble. Vuelva a tirar.')

    
    return jugador
jugador1 = tirada_dados(jugador1)
print('jugador1', jugador1)