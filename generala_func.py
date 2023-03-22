import random
from collections import defaultdict
import sys
import tabulate

dados_dic = {1:'       \n|       |\n|   *   |\n|       |\n       ', 
            2:'       \n| *     |\n|       |\n|     * |\n       ',
            3:'       \n|   *   |\n|   *   |\n|   *   |\n       ',
            4:'       \n| *   * |\n|       |\n| *   * |\n       ',
            5:'       \n| *   * |\n|   *   |\n| *   * |\n       ',
            6:'       \n| *   * |\n| *   * |\n| *   * |\n       '}
jugadas_grandes = {'Escalera':20, 'Full':30, 'Poker':40, 'Generala':50, 'Generala doble':100}
ubicacion_en_tablero = {'Numero de ronda':0,'Numero de tiro':1,'Escalera':2, 'Full':3, 'Poker':4, 'Generala':5, 'Generala doble':6, '1':7, '2':8, '3':9, '4':10, '5':11, '6':12, 'total':13}

class Jugador:
    def __init__(self, nombre:str, numero_partida, puntaje=None) -> None:
        self.nombre = nombre.capitalize()
        if puntaje is None:
            puntaje = [1,1,None,None,None,None,None,None,None,None,None,None,None,None]
        self.puntaje = puntaje
        self.numero_partida = numero_partida
    
    def __str__(self) -> str:
        return f'{self.nombre}'

def tirada(dados_elegidos:list) -> list:
    '''
    Realiza la tirada de dados. Toma una lista (vacia o no) y retorna una lista de dados arrojados
    '''
    dados_tirados = []
    _ = input('Presione una tecla para arrojar los dados: ')
    for _ in range((5-len(dados_elegidos))):
        dados_tirados.append(random.randint(1,6))
    dados_elegidos.extend(dados_tirados)
    dados_elegidos.sort()
    print(dados_elegidos)
    print(dados_dic[dados_elegidos[0]],dados_dic[dados_elegidos[1]],dados_dic[dados_elegidos[2]],dados_dic[dados_elegidos[3]],dados_dic[dados_elegidos[4]])
    return dados_elegidos

def elegir_dados(dados_elegidos:list) -> list:
    '''
    Toma los dados resultantes de la tirada y retorna los dados que el jugador desea conservar para el siguiente tiro
    '''
    dados= []
    print('Elige los dados que quieras guardar para el siguiente tiro...\n')
    for i in range(1, 6):
        print(f'{i}: {dados_elegidos[i-1]}')
    
    eleccion = input('\nEscribe el numero de menu de los dados a elegir, sin comas ni espacios: ')
    valid = set('12345')
    while not eleccion.isdigit() or not set(eleccion).issubset(valid):
        print('Por favor, ingrese la opción deseada: ')
        eleccion = input('\nEscribe el numero de menu de los dados a elegir, sin comas ni espacios: ')
    for i in eleccion:
        dados.append(dados_elegidos[int(i)-1])
    while True:
        x = input(f'Sus dados son:\n{dados}\n\nPresione 1 para confirmar o 2 para volver a elegir: ')
        if x == '1':
            return dados
        elif x == '2':
            return elegir_dados(dados_elegidos)
        else:
            print('Por favor, ingrese la opción deseada: ')

def check_jugadas_grandes(dados_elegidos:list,nro_tiro:int,jugador:object) -> list:
    '''
    Se ingresa el resultado de la tirada y el numero de tiro.
    Retorna una lista con las jugadas grandes del juego.
    El numero de tiro es importante para saber si se termina la partida(nro de tiro == 1 and Generala: fin del juego)
    '''
    jugadas = []
    if dados_elegidos == [1,2,3,4,5] or dados_elegidos == [2,3,4,5,6]:
        if jugador.puntaje[2] is None:
            jugadas.append('Escalera')
    if dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[0] == dados_elegidos[2] and dados_elegidos[3] == dados_elegidos[4] or dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[2] == dados_elegidos[3] and dados_elegidos[2] == dados_elegidos[4]:
        if jugador.puntaje[3] is None:
            jugadas.append('Full')
    if dados_elegidos[0] == dados_elegidos[3] or dados_elegidos[1] == dados_elegidos[4]:
        if jugador.puntaje[4] is None:
            jugadas.append('Poker')
    if dados_elegidos[0] == dados_elegidos[4]:
        if jugador.puntaje[5] is None:
            jugadas.append('Generala')
            if nro_tiro == 1:
                print(f'GENERALA SERVIDA!!!! {jugador.nombre} ha ganado el juego!!!')
                input(f'\nPresione una tecla para salir: ')
                cerrar_partida()
        elif jugador.puntaje[5] is not None:
            jugadas.append('Generala doble')
    return jugadas
    
def check_jugadas_chicas(dados_elegidos:list,jugador:object) -> list:
    '''
    Se ingresa una lista con los dados tirados y retorna las jugadas chicas en una lista
    '''
    jugadas_chicas_dic = defaultdict(int)
    for i in range(1,7):
            jugadas_chicas_dic[f'{i}'] = i * dados_elegidos.count(i)
    lista_jugadas_chicas = []
    for k,v in jugadas_chicas_dic.items():
        if v != 0 and jugador.puntaje[ubicacion_en_tablero[k]] is None:
            lista_jugadas_chicas.append(f'{v} al {k}')
    return lista_jugadas_chicas

def plantar(jugadas:list,jugador:object,nro_tiro:int) -> None:
        global jugadas_grandes
        global ubicacion_en_tablero
        eleccion = int(input('\nSeleccione el numero que corresponde a la jugada que quiere plantar: '))-1
        while eleccion > len(jugadas) or eleccion < 0: #esta es la validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            eleccion = int(input('seleccione el numero que corresponde a la jugada que quiere plantar'))
        if jugadas[eleccion] in jugadas_grandes:
            if nro_tiro == 1:
                jugadas.puntaje[ubicacion_en_tablero[jugadas[eleccion]]] = jugadas_grandes[jugadas[eleccion]] + 5
                jugador.puntaje[1] = 1
                
            else:
                jugador.puntaje[ubicacion_en_tablero[jugadas[eleccion]]] = jugadas_grandes[jugadas[eleccion]]
                jugador.puntaje[1] = 1
        else:
            if jugadas[eleccion][1:2].isspace():
                jugador.puntaje[ubicacion_en_tablero[jugadas[eleccion][-1:]]] = jugadas[eleccion][0:1]
                jugador.puntaje[1] = 1
            else:
                jugador.puntaje[ubicacion_en_tablero[jugadas[eleccion][-1:]]] = jugadas[eleccion][0:2]
                jugador.puntaje[1] = 1
        print(f'\nSe ha guardado la jugada {jugadas[eleccion]}\n')

def tachar(jugador:object) -> None:
    '''
    Se anula una de las posiciones en la tabla de puntajes
    '''
    global ubicacion_en_tablero
    ubicacion_invertida_en_tablero = {0:'Numero de ronda',1:'Numero de tiro',2:'Escalera',3:'Full',4: 'Poker', 5:'Generala', 6:'Generala doble', 7:'1', 8:'2', 9:'3', 10:'4',11: '5', 12:'6',13: 'total'}
    tachables = []
    print(f'\nPuede tachar las siguientes jugadas: \n')
    contador_menu = 1
    for i in range(2,13):
        if jugador.puntaje[i] is None:
            tachables.append(ubicacion_invertida_en_tablero[i])
            print(f'{contador_menu}: {ubicacion_invertida_en_tablero[i]}')
            contador_menu +=1
    entrada = input(f'Escriba la jugada que quiere tachar de la lista de arriba: ').capitalize()
    while entrada not in tachables:
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
        entrada = input(f'Escriba la jugada que quiere tachar de la lista de mas arriba: ')
    jugador.puntaje[ubicacion_en_tablero[entrada]] = 0
    print(f'\nSe ha tachado la siguiente jugada: {entrada}')

def menu_despues_de_tirada(dados_elegidos: list,nro_tiro:int,jugador:object) -> list:
    '''
    Se ingresan los dados al fin del tiro y se muestran las opciones disponibles
    '''
    grandes = check_jugadas_grandes(dados_elegidos, nro_tiro,jugador)
    chicas = check_jugadas_chicas(dados_elegidos,jugador)
    grandes.extend(chicas)
    for i,jug in enumerate(grandes, start=1):
        print(f'{i}- {jug}')
    if nro_tiro == 3:
        if len(grandes) == 0:
            tachar(jugador)
            return
        eleccion = input(f'\nPresione 1 para plantar o 2 para tachar una jugada: ')
        ref_anotacion = ["1","2"]
        while eleccion not in ref_anotacion: # esta es la validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            eleccion = input(f'\nPresione 1 para plantar o 2 para tachar una jugada: ')
        if eleccion == '1': # Planta
            plantar(grandes, jugador, nro_tiro)        
        elif eleccion == '2': # Tacha
            tachar(jugador)
    else:
        if len(grandes) == 0:
            eleccion = input(f'\nPresione 2 para seleccionar dados y volver a arrojar: ')
        else:
            eleccion = input(f'\nPresione 1 para elegir una de las jugadas y plantar o 2 para seleccionar dados y volver a arrojar: ')
        ref_anotacion = ["1","2"]
        while eleccion not in ref_anotacion: # esta es la validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            eleccion = input('\nPresione 1 para elegir una de las jugadas o 2 para seleccionar dados y volver a arrojar: ')
        if eleccion == '1': # Planta
            plantar(grandes, jugador, nro_tiro)        
        elif eleccion == '2':
            jugador.puntaje[1] += 1
            menu_despues_de_tirada(tirada(elegir_dados(dados_elegidos)),jugador.puntaje[1],jugador)

def guardar_borrar_partida(idPartida: int) -> None:
    '''
    Da la opcion de guardar y cerrar la partida o eliminarla y salir.
    '''
    print("Ingrese:\n- 1 para GUARDAR la partida y SALIR.\n- 2 para BORRAR la partida y SALIR.")
    ref_anotacion = ["1", "2"]
    opcion_continuar = input("\nIngrese la opción deseada: ")
    while opcion_continuar not in ref_anotacion: # esta es la validacion para un ingreso erróneo
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
        opcion_continuar = input("Ingrese:\n- 1 para GUARDAR la partida y SALIR.\n- 2 para BORRAR la partida y SALIR.")
    if opcion_continuar == '1': # Cierra la Base de Datos, cierra el juego y sale del programa
        #funcionesbd.cerrarBase()
        print("La partida ha sido guardada CORRECTAMENTE!")
        cerrar_partida()
    elif opcion_continuar == 2: # pide la confirmacion para borrar la partida que ha jugado
        ref_borrar = ["1", "2"]
        print("\nPor favor, confirme su eleccion.")
        borrar = input("Presione -> 1 para BORRAR y SALIR\nPresione -> 2 para VOLVER ATRÁS: ")
        while borrar not in ref_borrar: # validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            borrar = int(input("\nPresione -> 1 para BORRAR y SALIR\nPresione -> 2 para VOLVER ATRÁS: "))
        if borrar == "1": # borra la partida y sale del programa
            #funcionesbd.borrarPartida(idPartida)
            print("Partida borrada CORRECTAMENTE!.")
            cerrar_partida()
        elif borrar == "2": # vuelve a preguntar si desea continuar la partida
            pregunta_continuar(idPartida)

def pregunta_continuar(id_partida:int) -> bool:
    '''
    pregunta al usuario si desea continuar la partida o guardarla/borrarla
    '''
    print("Presione -> ENTER para CONTINUAR la partida.")
    opcion = input("Presione -> 1 para GUARDAR y SALIR: ")
    if opcion == "1": # esta opción lleva a otra función que amplía las opciones a guardar y salir, o borrar y salir.
        print("")
        guardar_borrar_partida(id_partida)
    else: # esta opcion hace que la partida continúe
        print("")
        return True
    
def cerrar_partida():
    '''
    Cierra el programa cuando el usuario lo desea o si finaliza la partida.
    '''
    print("Muchas gracias por jugar! Vuelva pronto!")
    input()
    sys.exit()

def sumar_puntajes(JUGADORES) -> None:
    #chequear BD
    puntajes_altos = []
    orden_puntajes = []
    for numero, jugador in JUGADORES.items():
        count = sum(jugador.puntaje[2:-1])
        jugador.puntaje[-1] = count
        if count > min(puntajes_altos):
            puntajes_altos.append((jugador.name, count))
            #guardar en bd
        orden_puntajes.append((jugador.nombre,count))
    tabla = sorted(orden_puntajes, key=lambda x: x[1], reverse=True)
    tablero = tabulate(tabla, headers=["Nombre", "Puntaje"])
    print(tablero)
    print(f'\n*** El jugador {tabla[0][0]} ha ganado la partida. FELICITACIONES!!! ***')


def nueva_partida():
    cant_jugadores = input('\nSeleccione la cantidad de jugadores: ')
    while not cant_jugadores.isdigit() or int(cant_jugadores) > 10:
        print('\nERROR! Lo ingresado no fue recibido correctamente.\nPor favor, ingrese una opción válida usando NÚMEROS.')
        cant_jugadores = input('\nSeleccione la cantidad de jugadores: ')
    JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
    numero_partida = 1#recolectar de BD el numero, puse 1 para probar
    for i in range(1, int(cant_jugadores)+1):
        x = input(f'\nElige el nombre del jugador {i}: ')
        JUGADORES[i] = Jugador(x,numero_partida)
        #Guardar jugadores en BD
    for turno in range(1,12):
        print(f'\n*** Ronda numero {turno} ***\n')
        for numero, jugador in JUGADORES.items():
            print(f'\nEs el turno del jugador #{numero}: {jugador.nombre}')
            dados_elegidos = tirada([])
            menu_despues_de_tirada(dados_elegidos,jugador.puntaje[1],jugador)
            jugador.puntaje[0] += 1
            if pregunta_continuar(numero_partida):
                pass
    sumar_puntajes(JUGADORES)
    volver_a_jugar = input(f'\nDesea volver a jugar?\nPresione 1 para volver a jugar o ENTER para finalizar\n')
    if volver_a_jugar == '1':
        nueva_partida()
    else:
        cerrar_partida()

def reanudar_partida(id_partida:int):
    JUGADORES = 'jugadores de la BD de esa partida'
    for _,jugador in JUGADORES.items():
        print(f'\nJugador #{_}: {jugador.nombre}\nPuntaje parcial:\n')
        headers = ['# Turno', '# Tiro', 'Escalera', 'Full', 'Poker', 'Generala', 'Generala doble', '1', '2', '3', '4', '5', '6']
        print(tabulate(jugador.puntaje[:-1], headers=headers, tablefmt="rst"))
        #ver de poner todos los puntajes juntos.
        #continuar los tiros desde donde lo dejamos.

        
def iniciarPrograma():
    '''
    La funcion que general que inicia todo el juego
    '''
    print(">>> BIENVENIDO A LA GENERALA! <<<")
    print("Desea iniciar una partida nueva?\nIngrese:\n- 1 para iniciar una NUEVA partida.\n- 2 para REANUDAR la ultima partida guardada.\n- 3 para ver PUNTAJES MAS ALTOS")
    print("- 4 para CERRAR el programa.")
    ref_anotacion = ['1','2','3','4']
    opcion_partida = input("\nIngrese la opción deseada: ")
    while opcion_partida not in ref_anotacion: # Esta es la validacion para un ingreso erróneo
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente.\nPor favor, ingrese una opción válida usando NÚMEROS.")
        print("- 1 para iniciar una nueva partida.\n- 2 para reanudar una partida guardada.\n- 3 para CERRAR el programa.")
        opcion_partida = input("\nPor favor, ingrese la opción deseada: ")
    if opcion_partida == '1': # invoca a la funcion de iniciar una partida nueva
        print("\nUsted ha iniciado una NUEVA PARTIDA.\n")
        nueva_partida()
    elif opcion_partida == '2': # invoca a la función de reanudar la ultima partida guardada
        print("\nUsted ha elegido reanudar la ultima partida.\n")
        id_partida = 'ULTIMA PARTIDA EN BD'
        reanudar_partida(id_partida)
    elif opcion_partida == '3': # Mejores puntajes
        #consultar BD por puntajes mas altos
        puntajes_altos = []
        print(tabulate(puntajes_altos, headers=['Nombre','Puntaje'], tablefmt='simple'))
    elif opcion_partida == '4': # cerrar el programa y salir del juego
        print("Muchas gracias por jugar! Vuelva Pronto!")
        cerrar_partida()
