import random
from collections import defaultdict
import sys

dados_dic = {1:'       \n|       |\n|   *   |\n|       |\n       ', 
            2:'       \n| *     |\n|       |\n|     * |\n       ',
            3:'       \n|   *   |\n|   *   |\n|   *   |\n       ',
            4:'       \n| *   * |\n|       |\n| *   * |\n       ',
            5:'       \n| *   * |\n|   *   |\n| *   * |\n       ',
            6:'       \n| *   * |\n| *   * |\n| *   * |\n       '}
jugadas_grandes = {'escalera':20, 'full':30, 'poker':40, 'generala':50, 'generala doble':100}
ubicacion_en_tablero = {'Numero de ronda':0,'Numero de tiro':1,'escalera':2, 'full':3, 'poker':4, 'generala':5, 'generala doble':6, '1':7, '2':8, '3':9, '4':10, '5':11, '6':12, 'total':13}

class Jugador:
    def __init__(self, nombre:str, numero_partida, puntaje=None) -> None:
        self.nombre = nombre.lower()
        if puntaje is None:
            puntaje = [1,1,None,None,None,None,None,None,None,None,None,None,None,None]
        self.puntaje = puntaje
        self.numero_partida = numero_partida
    
    def __str__(self) -> str:
        return f'{self.name}'


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

def check_jugadas_grandes(dados_elegidos:list,nro_tiro:int,jugador) -> list:
    '''
    Se ingresa el resultado de la tirada y el numero de tiro.
    Retorna una lista con las jugadas grandes del juego.
    El numero de tiro es importante para saber si se termina la partida(nro de tiro == 1 and generala: fin del juego)
    '''
    jugadas = []
    if dados_elegidos == [1,2,3,4,5] or dados_elegidos == [2,3,4,5,6]:
        jugadas.append('escalera')
    if dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[0] == dados_elegidos[2] and dados_elegidos[3] == dados_elegidos[4] or dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[2] == dados_elegidos[3] and dados_elegidos[2] == dados_elegidos[4]:
        jugadas.append('full')
    if dados_elegidos[0] == dados_elegidos[3] or dados_elegidos[1] == dados_elegidos[4]:
        jugadas.append('poker')
    if dados_elegidos[0] == dados_elegidos[4]:
        jugadas.append('generala')
        if nro_tiro == 1 and 'generala' in jugadas:
            print(f'GENERALA SERVIDA!!!! {jugador.name}ha ganado el juego!')
            #agregar fin del juego en este momento?
    return jugadas
    
def check_jugadas_chicas(dados_elegidos:list) -> list:
    '''
    Se ingresa una lista con los dados tirados y retorna las jugadas chicas en una lista
    '''
    jugadas_chicas_dic = defaultdict(int)
    for i in range(1,7):
            jugadas_chicas_dic[f'{i}'] = i * dados_elegidos.count(i)
    lista_jugadas_chicas = []
    for k,v in jugadas_chicas_dic.items():
        if v != 0:
            lista_jugadas_chicas.append(f'{v} al {k}')
    return lista_jugadas_chicas

def menu_despues_de_tirada(dados_elegidos: list,nro_tiro:int,jugador) -> list:
    '''
    Se ingresan los dados al fin del tiro y se muestra en pantalla todas las jugadas posibles
    '''
    grandes = check_jugadas_grandes(dados_elegidos, nro_tiro,jugador)
    chicas = check_jugadas_chicas(dados_elegidos)
    grandes.extend(chicas)
    for i,jug in enumerate(grandes, start=1):
        print(f'{i}- {jug}')
    eleccion = input(f'\nPresione 1 para elegir una de las jugadas y plantar o 2 para seleccionar dados y volver a arrojar: ')
    ref_anotacion = {"1": 1, "2": 2}
    while eleccion not in ref_anotacion: # esta es la validacion para un ingreso erróneo
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
        eleccion = input('\nPresione 1 para elegir una de las jugadas o 2 para seleccionar dados y volver a arrojar: ')
    if eleccion == '1': # Planta
        eleccion_jugada = int(input('seleccione el numero que corresponde a la jugada que quiere plantar'))-1
        while eleccion_jugada > len(grandes) or eleccion_jugada < 0: #esta es la validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            eleccion = int(input('seleccione el numero que corresponde a la jugada que quiere plantar'))
        if grandes[eleccion] in jugadas_grandes:
            if nro_tiro == 1:
                jugador.puntaje[ubicacion_en_tablero[grandes[eleccion]]] = jugadas_grandes[grandes[eleccion]] + 5
            else:
                jugador.puntaje[ubicacion_en_tablero[grandes[eleccion]]] = jugadas_grandes[grandes[eleccion]]
        else:
            if grandes[eleccion][1:2].isspace():
                jugador.puntaje[ubicacion_en_tablero[grandes[eleccion][-1:]]] = grandes[eleccion][0:1]
            else:
                jugador.puntaje[ubicacion_en_tablero[grandes[eleccion][-1:]]] = grandes[eleccion][0:2]
    elif eleccion == '2':
        elegir_dados(dados_elegidos)

def guardar_borrar_partida(idPartida):
    '''
    Da la opcion de guardar y cerrar la partida o eliminarla y salir.
    '''
    print("Ingrese:\n- 1 para GUARDAR la partida y SALIR.\n- 2 para BORRAR la partida y SALIR.")
    ref_anotacion = {"1": 1, "2": 2}
    opcion_continuar = input("\nIngrese la opción deseada: ")
    while opcion_continuar not in ref_anotacion: # esta es la validacion para un ingreso erróneo
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
        opcion_continuar = int(input("Ingrese:\n- 1 para GUARDAR la partida y SALIR.\n- 2 para BORRAR la partida y SALIR."))
    if opcion_continuar == 1: # Cierra la Base de Datos, cierra el juego y sale del programa
        #funcionesbd.cerrarBase()
        print("La partida ha sido guardada CORRECTAMENTE!")
        print("Muchas gracias por jugar! Vuelva pronto!")
        sys.exit()
    elif opcion_continuar == 2: # pide la confirmacion para borrar la partida que ha jugado
        ref_borrar = {"1": 1, "2": 2}
        print("\nPor favor, confirme su eleccion.")
        borrar = int(input("Presione -> 1 para BORRAR y SALIR\nPresione -> 2 para VOLVER ATRÁS: "))
        while borrar not in ref_borrar: # validacion para un ingreso erróneo
            print("\n*** ERROR! Lo ingresado no fue recibido correctamente. Por favor, ingrese una opción válida.")
            borrar = int(input("\nPresione -> 1 para BORRAR y SALIR\nPresione -> 2 para VOLVER ATRÁS: "))
        if borrar == "1": # borra la partida y sale del programa
            #funcionesbd.borrarPartida(idPartida)
            print("Partida borrada CORRECTAMENTE!.\nMuchas gracias por jugar! Vuelva pronto!")
            sys.exit()
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
    sys.exit()

def nueva_partida():
    cant_jugadores = input('\nSeleccione la cantidad de jugadores: ')
    while not cant_jugadores.isdigit() or int(cant_jugadores) > 10:
        print('\nERROR! Lo ingresado no fue recibido correctamente.\nPor favor, ingrese una opción válida usando NÚMEROS.')
        cant_jugadores = input('\nSeleccione la cantidad de jugadores: ')
    JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
    numero_partida = 1 #recolectar de BD el numero, puse 1 para probar
    for i in range(1, cant_jugadores+1):
        x = input(f'\nElige el nombre del jugador {i}')
        JUGADORES[i] = Jugador(x,numero_partida)
        

def iniciarPrograma():
    '''
    La funcion que general que inicia todo el juego
    '''
    print(">>> BIENVENIDO A LA GENERALA! <<<")
    print("Desea iniciar una partida nueva?\nIngrese:\n- 1 para iniciar una NUEVA partida.\n- 2 para REANUDAR una partida guardada.")
    print("- 3 para CERRAR el programa.")
    ref_anotacion = {"1": 1, "2": 2, "3": 3}
    opcion_partida = input("\nIngrese la opción deseada: ")
    while opcion_partida not in ref_anotacion: # Esta es la validacion para un ingreso erróneo
        print("\n*** ERROR! Lo ingresado no fue recibido correctamente.\nPor favor, ingrese una opción válida usando NÚMEROS.")
        print("- 1 para iniciar una nueva partida.\n- 2 para reanudar una partida guardada.\n- 3 para CERRAR el programa.")
        opcionPartida = input("\nPor favor, ingrese la opción deseada: ")
    opcionPartida = int(opcionPartida)
    if opcionPartida == 1: # invoca a la funcion de iniciar una partida nueva
        print("\nUsted a iniciado una NUEVA PARTIDA.\n")
        nueva_partida()
    elif opcionPartida == 2: # invoca a la función de reanudar una partida guardada
        print("")
        #reanudarPartida()
    elif opcionPartida == 3: # cerrar el programa y salir del juego
        print("Muchas gracias por jugar! Vuelva Pronto!")
        cerrar_partida()
