import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from collections import defaultdict
import random
import sys


ubicacion_en_tablero = {'Numero de ronda':0,'Numero de tiro':1,'Escalera':2, 'Full':3, 'Poker':4, 'Generala':5, 'Generala doble':6, '1':7, '2':8, '3':9, '4':10, '5':11, '6':12, 'total':13}

#Creacion de la clase Jugador
class Jugador:
    def __init__(self, nombre:str, numero_partida, puntaje=None) -> None:
        self.nombre = nombre.capitalize()
        if puntaje is None:
            puntaje = [1,1,None,None,None,None,None,None,None,None,None,None,None,None]
        self.puntaje = puntaje
        self.numero_partida = numero_partida
    
    def __str__(self) -> str:
        return f'{self.nombre}\nPuntaje: {self.puntaje}\n'
    
def submit(entrada, entry):#El uso principal es para poder implementar el wait_variable mas adelante
    '''
    Al presionar el boton Submit, entrada se modifica.
    '''
    entrada.set(entry.get())

def tirada(dados_elegidos, entry, entrada, boton_submit) -> list:
    '''
    Realiza la tirada de dados. Toma una lista (vacia o no) y retorna una lista de dados arrojados
    '''
    dados_tirados = []
    boton_submit.wait_variable(entrada)
    for _ in range((5-len(dados_elegidos))):
        dados_tirados.append(random.randint(1,6))
    dados_elegidos.extend(dados_tirados)
    dados_elegidos.sort()
    print(dados_elegidos)
    print(dados_dic[dados_elegidos[0]],dados_dic[dados_elegidos[1]],dados_dic[dados_elegidos[2]],dados_dic[dados_elegidos[3]],dados_dic[dados_elegidos[4]])
    return dados_elegidos

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

def nueva_partida(root, entrada, entry, boton_submit, boton_n_partida, boton_r_partida, boton_puntajes_altos, frame_izq, label_ronda_frameizq, label_jugador_frameizq, frame_der):
    '''
    Comienza nueva partida.
    '''
    #modifica la pantalla principal
    boton_n_partida.place_forget()
    boton_r_partida.place_forget()
    boton_puntajes_altos.place_forget()
    boton_submit.configure(text='Enter!', fg_color='blue',state='normal')
    
    #comienza la ejecucion del juego
    label = ctk.CTkLabel(master=root, text='Selecciona la cantidad de jugadores: ', font=('roboto',24))
    label.place(relx=0.20, rely=0.30)
    boton_submit.wait_variable(entrada)
    cant_jugadores = entry.get()
    while not cant_jugadores.isdigit() or int(cant_jugadores) > 10 or int(cant_jugadores) < 1: #Validacion de entrada y cantidad de jugadores
        CTkMessagebox(title='Generala', icon = 'cancel', message = 'Seleccione la cantidad de jugadores (1-10) usando NUMEROS', option_1 = 'OK', button_color='blue')
        boton_submit.wait_variable(entrada)
        cant_jugadores = entry.get()
    JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
    numero_partida = 1#recolectar de BD el numero, puse 1 para probar
    entry.delete(0, ctk.END) #Reinicia el texto del entry box

    for i in range(1, int(cant_jugadores)+1): #Seleccion de los nombres de los jugadores
        label.configure(text=f'Elige el nombre del jugador {i}:')
        boton_submit.wait_variable(entrada) #Hacer que el codigo espere a que se presione boton de submit
        x = entry.get()
        while not x.isalpha(): #Validacion de entrada y cantidad de jugadores
            CTkMessagebox(title='Generala', icon = 'cancel', message = 'Seleccione el nombre del jugador utilizando solo LETRAS', option_1 = 'OK', button_color='blue')
            boton_submit.wait_variable(entrada)
            x = entry.get()
        JUGADORES[i] = Jugador(x,numero_partida) #Se crea una instancia de la clase Jugador con el nombre que se escribio previamente
        entry.delete(0, ctk.END)
    frame_izq.grid(row=0, column=0, rowspan=4, sticky="nsew")
    frame_der.grid(row=0, column=8, rowspan=4, sticky="nsew")
    boton_submit.configure(text='Tirar!', fg_color='red', border_color='#cc0000')
    entry.configure(state='disabled')


    for turno in range(1,12): #Bucle para la ejecucion de los turnos
        label_ronda_frameizq.configure(text=f'Ronda numero {turno}', font=('roboto', 14, 'bold'))
        label_ronda_frameizq.place(relx=0.2, rely=0.02)

        for numero, jugador in JUGADORES.items(): #Dentro de cada turno, bucle para la ejecucion del tiro de cada jugador
            label_jugador_frameizq.configure(text=f'Jugador: {jugador.nombre}', font=('roboto', 14, 'bold'))
            label_jugador_frameizq.place(relx=0.2, rely=0.2)
            label.configure(text=f'Es el turno del jugador #{numero}: {jugador.nombre}')
            boton_submit.wait_variable(entrada)
            dados_elegidos = tirada([], entry, entrada, boton_submit)
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

def reanudar_partida(numero_partida:int):
    '''
    Toma como parametro la ultima partida y la retoma de donde quedó
    '''
    llamado_BD = 'jugadores de la BD de esa partida' #Iterar para crear instancias de la clase jugador
    JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
    for _,jugador in JUGADORES.items():
        print(f'\nJugador #{_}: {jugador.nombre}\nPuntaje parcial:\n')
        headers = ['# Turno', '# Tiro', 'Escalera', 'Full', 'Poker', 'Generala', 'Generala doble', '1', '2', '3', '4', '5', '6']
        print(tabulate(jugador.puntaje[:-1], headers=headers, tablefmt="rst"))
    ronda = JUGADORES[1].puntaje[0]
    for turno in range(ronda,12):
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

def cerrar_programa(root):
    '''
    Crea una alerta al intentar cerrar el programa, pide confirmacion para cerrar.
    '''
    mensaje = CTkMessagebox(title="Exit?", message="Quieres cerrar el programa?",
                        icon="question", option_1="Cancelar", option_2="Cerrar")
    respuesta = mensaje.get()
    if respuesta=="Cerrar":
        root.destroy()
    elif respuesta == 'Cancelar':
        return

def puntajes_altos(root,bienvenido, boton_n_partida, boton_r_partida, boton_puntajes_altos):
    '''
    Muestra los 10 puntajes mas altos conseguidos en el juego
    '''
    #llamar a la BBDD y conseguir los 10 puntajes mas altos
    string_puntajes_altos = f'1 - 250  PEPE\n2 - 240  CARLOS\n3 = 230  JUAN\n4 = 220  JUAN\n5 = 210  JUAN\n6 = 200  JUAN\n7 = 190  JUAN\n8 = 180  JUAN\n9 = 170  JUAN\n10 = 150  JUAN'
    
    bienvenido.place_forget()
    boton_n_partida.place_forget()
    boton_r_partida.place_forget()
    boton_puntajes_altos.place_forget()
    header_puntajes = ctk.CTkLabel(root, text='PUNTAJES MAS ALTOS', font=('roboto',60,'bold'))
    header_puntajes.place(relx= 0.25, rely=0.12)
    puntajes_altos_label = ctk.CTkLabel(master=root, width=300,text=string_puntajes_altos, font=('roboto',24),justify='left')
    puntajes_altos_label.place(relx= 0.45, rely=0.30)
    boton_vuelta = ctk.CTkButton(master=root, width=100, text='Volver',fg_color='blue',font=('roboto',14), command=lambda: boton_volver(bienvenido, puntajes_altos_label, header_puntajes, boton_vuelta, boton_n_partida, boton_r_partida, boton_puntajes_altos))
    boton_vuelta.place(relx= 0.20, rely=0.05)

def boton_volver(bienvenido, puntajes_altos_label, header_puntajes, boton_vuelta, boton_n_partida, boton_r_partida, boton_puntajes_altos):
    puntajes_altos_label.place_forget()
    header_puntajes.place_forget()
    boton_vuelta.place_forget()
    bienvenido.place(relx= 0.20, rely=0.10)
    boton_n_partida.place(relx= 0.48, rely=0.30)
    boton_r_partida.place(relx= 0.48, rely=0.45)
    boton_puntajes_altos.place(relx= 0.48, rely=0.60)