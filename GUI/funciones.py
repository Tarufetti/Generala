import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from collections import defaultdict
from PIL import Image
import random
import os

cwd = os.getcwd()
UBICACION_EN_TABLERO = {'Numero de ronda':0,'Numero de tiro':1,'1':2, '2':3, '3':4, '4':5, '5':6, '6':7, 'Escalera':8, 'Full':9, 'Poker':10, 'Generala':11, 'Generala Doble':12, 'total':13}
LISTA_JUGADAS = ['1','2','3','4','5','6','Escalera','Full','Poker','Generala','Generala Doble','Total']
PUNTAJES_JUGADAS = {'Escalera':20, 'Full':30, 'Poker':40, 'Generala':50,'Generala Doble':100}
dice = []
dados_elegidos = []
jugadas_tiro_actual = []
booleano = True




#Creacion de la clase Jugador
class Jugador:
    def __init__(self, nombre, numero_partida, puntaje=None):
        self.nombre = nombre.capitalize()
        if puntaje is None:
            puntaje = [1,1,None,None,None,None,None,None,None,None,None,None,None,None]
        self.puntaje = puntaje
        self.numero_partida = numero_partida
    
    def __str__(self):
        return f'{self.nombre}\nPuntaje: {self.puntaje}\n'

def submit(entrada, entry):#El uso principal es para poder implementar el wait_variable mas adelante
    '''
    Al presionar el boton Submit, entrada se modifica.
    '''
    entrada.set(entry.get())

def tirada(dados_elegidos, dice, entrada, boton_submit, root, label, img_dados_generico):
    '''
    Realiza la tirada de dados. Toma una lista (vacia o no) y retorna una lista de dados arrojados
    '''
    dados_tirados = []
    boton_submit.wait_variable(entrada)
    label.place_forget()
    for _ in range((5-len(dados_elegidos))):
        dados_tirados.append(random.randint(1,6))
    dados_elegidos.extend(dados_tirados)
    dados_elegidos.sort()

    #Creacion de las imagenes de dados
    for i in range(5):
        img_dados_generico[i].place_forget()
        if len(dice) == 5:
            dice[i].place_forget()
    dice.clear()
    dice_relx = 0.20 # incrementa de a 0.12 para mantener simetria
    dice_rely = 0.15
    for i in dados_elegidos:
        img = ctk.CTkImage(Image.open(f'{cwd}/resources/dice{i}.png'),size=(100,100))
        img_label = ctk.CTkLabel(master=root,text='', image=img)
        img_label.place(relx=dice_relx, rely=dice_rely)
        dice.append(img_label)
        dice_relx += 0.12
    return dados_elegidos

def check_jugadas_grandes(dados_elegidos,nro_tiro,jugador):
    '''
    Se ingresa el resultado de la tirada y el numero de tiro.
    Retorna una lista con las jugadas grandes del juego.
    El numero de tiro es importante para saber si se termina la partida(nro de tiro == 1 and Generala: fin del juego)
    '''
    jugadas = []
    if dados_elegidos == [1,2,3,4,5] or dados_elegidos == [2,3,4,5,6]:
        if jugador.puntaje[2] is None:
            jugadas.append('Escalera')
    if dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[0] == dados_elegidos[2] and dados_elegidos[3] == dados_elegidos[4] and dados_elegidos[0] != dados_elegidos[4] or dados_elegidos[0] == dados_elegidos[1] and dados_elegidos[2] == dados_elegidos[3] and dados_elegidos[2] == dados_elegidos[4] and dados_elegidos[0] != dados_elegidos[4]:
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
    
def check_jugadas_chicas(dados_elegidos,jugador):
    '''
    Se ingresa una lista con los dados tirados y retorna las jugadas chicas en una lista
    '''
    jugadas_chicas_dic = defaultdict(int)
    for i in range(1,7):
            jugadas_chicas_dic[f'{i}'] = i * dados_elegidos.count(i)
    lista_jugadas_chicas = []
    for k,v in jugadas_chicas_dic.items():
        if v != 0 and jugador.puntaje[UBICACION_EN_TABLERO[k]] is None:
            lista_jugadas_chicas.append(f'{v} al {k}')
    return lista_jugadas_chicas

def elegir_dados(jugador, root, entrada, boton_submit, boton_elegir_dados, boton_plantar,label_tiro_frameizq, dados=dados_elegidos) -> list:
    '''
    Toma los dados resultantes de la tirada y retorna los dados que el jugador desea conservar para el siguiente tiro
    '''
    global dados_elegidos
    dados= []
    boton_elegir_dados.place_forget()
    boton_plantar.place_forget()
    boton_submit.configure(text='Confirmar!', fg_color='blue', state='normal', hover_color='light blue')
    #Creacion de los checkboxes
    checkboxes = []
    check_relx = 0.23 #incrementa de a 0.12
    check_rely = 0.40
    for i in range(1,6):
        checkbox = ctk.CTkCheckBox(master=root, text=f'{i}')
        checkbox.place(relx=check_relx, rely=check_rely)
        check_relx += 0.12
        checkboxes.append(checkbox)
    boton_submit.wait_variable(entrada)

    for i,check in enumerate(checkboxes):
        if check.get():
            dados.append(dados_elegidos[i])
    
    boton_submit.configure(text='Tirar!', fg_color='red', border_color='#cc0000', hover_color='red')
    for i in checkboxes:
        i.place_forget()
    dados.sort()
    dados_elegidos = dados

    jugador.puntaje[1] += 1
    label_tiro_frameizq.configure(text=f'Tiro #{jugador.puntaje[1]}')
    return dados_elegidos

def plantar(jugador, entry, entrada, label, boton_submit, boton_elegir_dados, boton_plantar, boton_tachar):
    
    global jugadas_tiro_actual
    global booleano
    global dados_elegidos

    #limpiar el centro de la GUI
    boton_tachar.place_forget()
    boton_plantar.place_forget()
    boton_elegir_dados.place_forget()
    label.configure(text='Elija la jugada que desea plantar: ', font=('roboto',18))

    jugadas = check_jugadas_grandes(dados_elegidos, jugador.puntaje[1],jugador)
    jugadas.extend(check_jugadas_chicas(dados_elegidos,jugador))

    #activar boton submit y entrada de texto
    boton_submit.configure(text='Confirmar!', fg_color='blue', state='normal', hover_color='light blue')
    entry.configure(state='normal')
    boton_submit.wait_variable(entrada)
    x = entry.get()
    while not x.isdigit() or int(x)<=0 or int(x)>len(jugadas): #Validacion de entrada
        CTkMessagebox(title='Generala', icon = 'cancel', message = f'Seleccione la jugada utilizando un NUMERO del 1 al {len(jugadas)}', option_1 = 'OK', button_color='blue')
        boton_submit.wait_variable(entrada)
        x = entry.get()
    entry.delete(0, ctk.END) #Reinicia el texto del entry box
    entry.configure(state='disabled') #Deshabilita el entry box

    for i in jugadas_tiro_actual:
        i.place_forget()
    jugadas_tiro_actual.clear()

    #Seleccion de jugada a plantar (jugadas grandes es 1 elemento en la lista, generala doble 2 y las jugadas chicas 3(x al y))
    lista_jugada_plantar = jugadas[int(x)-1].split()
    if len(lista_jugada_plantar) == 2:
        jugada_plantar = 'Generala Doble'
    else:
        jugada_plantar = lista_jugada_plantar[-1]

    if len(lista_jugada_plantar) > 2:
        jugador.puntaje[UBICACION_EN_TABLERO[jugada_plantar]] = int(lista_jugada_plantar[0]) # jugada chica
    else:
        jugador.puntaje[UBICACION_EN_TABLERO[jugada_plantar]] = PUNTAJES_JUGADAS[jugada_plantar] #jugada grande
    
    if jugador.puntaje[1] == 1:
        if jugada_plantar == 'Escalera' or jugada_plantar == 'Generala' or jugada_plantar == 'Generala Doble':
            label.configure(text=f'Se ha plantado la siguiente jugada: \n {jugadas[int(x)-1]} servida', font=('roboto',18))
            jugador.puntaje[UBICACION_EN_TABLERO[jugada_plantar]] += 5
        elif jugada_plantar == 'Full' or jugada_plantar == 'Poker':
            label.configure(text=f'Se ha plantado la siguiente jugada: \n {jugadas[int(x)-1]} servido', font=('roboto',18))
            jugador.puntaje[UBICACION_EN_TABLERO[jugada_plantar]] += 5
        else:
            label.configure(text=f'Se ha plantado la siguiente jugada: \n {jugadas[int(x)-1]}', font=('roboto',18))
    else:
        label.configure(text=f'Se ha plantado la siguiente jugada: \n {jugadas[int(x)-1]}', font=('roboto',18))

    boton_submit.wait_variable(entrada)

    jugador.puntaje[1] = 1 #reinicia tiro a #1
    dados_elegidos = [] #reinicia los dados
    booleano = False #Continua la ejecucion del bucle de juego
    boton_submit.configure(text='Tirar!', fg_color='red', border_color='#cc0000', hover_color='red')

def tachar(jugador, root, entry, entrada, boton_plantar, boton_tachar, boton_submit, label):
    '''
    Se anula una de las posiciones en la tabla de puntajes
    '''
    global jugadas_tiro_actual
    global booleano
    global dados_elegidos

    #limpiar el centro de la GUI
    boton_plantar.place_forget()
    boton_tachar.place_forget()
    
    #activar boton submit
    boton_submit.configure(text='Confirmar!', fg_color='blue', state='normal', hover_color='light blue')

    #opciones disponibles para tachar
    label.configure(text='Elija la jugada que desea tachar: ', font=('roboto',18))
    for i in jugadas_tiro_actual:
        i.place_forget()
    jugadas_tiro_actual.clear()
    tachables = []
    indice_tachables = 1
    rely = 0.50
    rely2= 0.50
    for ind,j in enumerate(jugador.puntaje[2:-1]):
        if j is None:
            label_tachables = ctk.CTkLabel(master=root, text=(f'{indice_tachables}- {LISTA_JUGADAS[ind]}                '), font=('roboto',14))
            jugadas_tiro_actual.append(label_tachables)
        indice_tachables +=1
        tachables.append(f'{LISTA_JUGADAS[ind]}')
    if len(jugadas_tiro_actual) >= 6:
        for ind,_ in enumerate(jugadas_tiro_actual):
            if ind < 6:
                _.place(relx=0.20, rely=rely)
                rely += 0.05
            elif ind >=6:
                _.place(relx=0.40, rely=rely2)
                rely2 += 0.05
    else:
        for _ in jugadas_tiro_actual:
            _.place(relx=0.20, rely=rely)
            rely += 0.05
    entry.configure(state='normal')
    boton_submit.wait_variable(entrada)
    x = entry.get()
    while not x.isdigit(): #Validacion de entrada
        CTkMessagebox(title='Generala', icon = 'cancel', message = 'Seleccione la jugada utilizando NUMEROS', option_1 = 'OK', button_color='blue')
        boton_submit.wait_variable(entrada)
        x = entry.get()
    entry.delete(0, ctk.END) #Reinicia el texto del entry box
    entry.configure(state='disabled')
    label.configure(text=f'Se ha tachado la siguiente jugada: \n {tachables[int(x)-1]}', font=('roboto',18))

    for i in jugadas_tiro_actual:
        i.place_forget()
    jugadas_tiro_actual.clear()

    boton_submit.wait_variable(entrada)
    jugador.puntaje[UBICACION_EN_TABLERO[tachables[int(x)-1]]] = 0 #modifica el valor de determinada jugada, de None a 0, para indicar que esta anulada. en GUI figura X
    jugador.puntaje[1] = 1 #reinicia tiro a #1

    dados_elegidos = []
    booleano = False
    boton_submit.configure(text='Tirar!', fg_color='red', border_color='#cc0000', hover_color='red')

def sumar_puntajes_individual(jugador):
    '''
    Suma del total de punto de un jugador
    '''
    total = 0
    for i in jugador.puntaje[2:13]:
        if i is not None:
            total += i
    jugador.puntaje[13] = total

def sumar_puntajes_total(JUGADORES):
    '''
    Suma de los puntajes totales de todos los jugadores, determina el ganador
    '''
    lista_puntajes_totales = []
    for _, i in JUGADORES.items():
        lista_puntajes_totales.append((i, i.puntaje[13] if i.puntaje[13] is not None else 0))
    lista_ordenada = sorted(lista_puntajes_totales, key=lambda x: x[1], reverse=True)
    jugadores_mismo_puntaje = []
    try:        
        if lista_ordenada[0][1] == lista_ordenada[1][1]: #Si los 2 jugadores con puntajes mas altos tienen el mismo puntaje, hay empate
            puntaje_igual = lista_ordenada[0][1]
            for i in lista_ordenada:
                if i[1] == puntaje_igual:
                    jugadores_mismo_puntaje.append(i[0])
    except IndexError: jugadores_mismo_puntaje.append(lista_ordenada[0][0])
    
    return lista_ordenada

def menu_despues_de_tirada(dados_elegidos, nro_tiro, jugador, root, entrada, label, boton_submit, boton_elegir_dados, boton_plantar, boton_tachar):
    '''
    Se ingresan los dados al fin del tiro y se muestran las opciones disponibles
    '''
    global jugadas_tiro_actual
    for i in jugadas_tiro_actual: # reiniciar la lista de jugadas para el tiro actual
        i.place_forget()
    jugadas_tiro_actual.clear()

    grandes = check_jugadas_grandes(dados_elegidos, nro_tiro,jugador)
    chicas = check_jugadas_chicas(dados_elegidos,jugador)
    grandes.extend(chicas)
    
    label.place_forget()
    label.configure(text='Jugadas: ', font=('roboto',18))
    label.place(relx=0.20, rely=0.45)
    
    for i,jug in enumerate(grandes, start=1):
        label_lista_jugadas = ctk.CTkLabel(master=root, text=(f'{i}- {jug}                '), font=('roboto',16))
        jugadas_tiro_actual.append(label_lista_jugadas)
    rely = 0.50
    for i in jugadas_tiro_actual:
        i.place(relx=0.20, rely=rely)
        rely += 0.05
    boton_submit.configure(text='', state='disabled', fg_color='grey')
    if nro_tiro == 3:
        if len(grandes) == 0:
            boton_tachar.place(relx=0.35, rely=0.80)
            return
        boton_plantar.place(relx=0.30, rely=0.80)
        boton_tachar.place(relx=0.45, rely=0.80)
    else:
        if len(grandes) == 0:
            boton_elegir_dados.place(relx=0.35, rely=0.80)
        else:
            boton_elegir_dados.place(relx=0.30, rely=0.80)
            boton_plantar.place(relx=0.45, rely=0.80)

def nueva_partida(root, entrada, entry, boton_submit, boton_n_partida, boton_r_partida, boton_puntajes_altos, frame_izq, label_ronda_frameizq, label_jugador_frameizq, label_tiro_frameizq, grilla_puntajes_izq, grilla_puntajes_der, frame_der, label_frameder, bienvenido, img_dados_generico, boton_elegir_dados, boton_plantar):
    '''
    Comienza nueva partida.
    '''
    global booleano

    def imagen_generica():
        '''
        Colocar imagen genérica previa a la tirada
        '''
        dice_relx = 0.20 # incrementa de a 0.12 para mantener simetria
        dice_rely = 0.12
        if len(dice) == 5:
            for i in range(5):
                dice[i].place_forget()
                img_dados_generico[i].place(relx=dice_relx, rely=dice_rely)
                dice_relx += 0.12
        else:
            for i in range(5):
                img_dados_generico[i].place(relx=dice_relx, rely=dice_rely)
                dice_relx += 0.12
                
    #modifica la pantalla principal
    boton_n_partida.place_forget()
    boton_r_partida.place_forget()
    boton_puntajes_altos.place_forget()
    boton_submit.configure(text='Enter!', fg_color='blue',state='normal')

    #Creacion botones elegir, plantar y tachar
    boton_elegir_dados =ctk.CTkButton(master=root, width=150, height=50 , text='Elegir dados', font=('roboto', 16), fg_color="blue", state='normal', command=lambda: menu_despues_de_tirada(tirada(elegir_dados(jugador, root, entrada, boton_submit, boton_elegir_dados, boton_plantar, label_tiro_frameizq), dice, entrada, boton_submit, root, label, img_dados_generico), jugador.puntaje[1],jugador, root, entrada, label, boton_submit, boton_elegir_dados, boton_plantar, boton_tachar))
    boton_plantar = ctk.CTkButton(master=root, width=150, height=50, text='Plantar', font=('roboto', 16), fg_color="blue", state='normal', command=lambda: plantar(jugador, entry, entrada, label, boton_submit, boton_elegir_dados, boton_plantar, boton_tachar))
    boton_tachar = ctk.CTkButton(master=root, width=150, height=50, text='Tachar Jugada', font=('roboto', 16), fg_color="blue", state='normal', command=lambda: tachar(jugador, root, entry, entrada, boton_plantar, boton_tachar, boton_submit, label))

    
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
    entry.delete(0, ctk.END) #Reinicia el texto del entry box
    numero_partida = 1#recolectar de BD el numero, puse 1 para probar

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
    boton_submit.configure(text='Tirar!', fg_color='red', border_color='#cc0000', hover_color='red')
    bienvenido.place_forget()

    entry.configure(state='disabled')
    
    #Configuracion grilla de puntajes izquierda
    id_elemento_izq = 0
    tag_grilla_izq= 'par'
    for i in LISTA_JUGADAS:
        grilla_puntajes_izq.insert("",'end', iid=id_elemento_izq, text=i, values=('0'), tags=(f'{tag_grilla_izq}'))
        id_elemento_izq +=1
        if tag_grilla_izq == 'par':
            tag_grilla_izq = 'impar'
        else : tag_grilla_izq = 'par'
        grilla_puntajes_izq.tag_configure('par', background='white')
        grilla_puntajes_izq.tag_configure('impar', background='light blue')
    grilla_puntajes_izq.place(relx=0.1,rely=0.3)

    #Configuracion grilla de puntajes derecha
    id_elemento_der = 0
    tag_grilla_der = 'par'
    for numero, jugador in JUGADORES.items():
        grilla_puntajes_der.insert("",'end', iid=id_elemento_der, text=jugador.nombre, values=('0'), tags=(f'{tag_grilla_der}'))
        id_elemento_der +=1
        if tag_grilla_der == 'par':
            tag_grilla_der = 'impar'
        else : tag_grilla_der = 'par'
        grilla_puntajes_der.tag_configure('par', background='white')
        grilla_puntajes_der.tag_configure('impar', background='light blue')
    grilla_puntajes_der.place(relx=0.1,rely=0.3)

    for turno in range(1,12): #Bucle para la ejecucion de los turnos

        #Numero de ronda de la partida en curso
        label_ronda_frameizq.configure(text=f'Ronda #: {turno} ', font=('roboto', 24, 'bold'))
        label_ronda_frameizq.place(relx=0.2, rely=0.02)
        label_frameder.place(relx=0.2, rely=0.02)

        for numero, jugador in JUGADORES.items(): #Dentro de cada turno, bucle para la ejecucion del tiro de cada jugador

            #Panel izquierdo con la información del jugador y su numero de tiro
            label_jugador_frameizq.configure(text=f'Jugador:\n{jugador.nombre}', font=('roboto', 20, 'bold'))
            label_jugador_frameizq.place(relx=0.2, rely=0.22)
            label_tiro_frameizq.configure(text=f'Tiro #: {jugador.puntaje[1]}', font=('roboto', 24, 'bold'))
            label_tiro_frameizq.place(relx=0.2, rely=0.06)
            
            #Tabla con el puntaje parcial del jugador
            indice_puntaje = 1
            for i in range(id_elemento_izq-1):
                indice_puntaje +=1
                grilla_puntajes_izq.item(str(i), values=(f'X' if jugador.puntaje[indice_puntaje] == 0 else jugador.puntaje[indice_puntaje]) if jugador.puntaje[indice_puntaje] is not None else 0)
            grilla_puntajes_izq.item('11', values=(jugador.puntaje[13]) if jugador.puntaje[13] is not None else 0) #Total aparte para evitar que sea 'X' cuando total es 0

            #Tabla con el puntaje total de todos los jugadores
            puntajes_totales = sumar_puntajes_total(JUGADORES)
            for i,val in enumerate(puntajes_totales):
                grilla_puntajes_der.item(str(i), text=val[0].nombre, values=(f'{val[1]}'))

            imagen_generica()

            label.configure(text=f'Es el turno del jugador #{numero}: {jugador.nombre}')
            menu_despues_de_tirada(tirada(dados_elegidos, dice, entrada, boton_submit, root, label, img_dados_generico), jugador.puntaje[1], jugador, root, entrada, label, boton_submit, boton_elegir_dados, boton_plantar, boton_tachar)
            while booleano:
                boton_submit.wait_variable(entrada)
            sumar_puntajes_individual(jugador)
            jugador.puntaje[0] += 1
            booleano = True
    total = sumar_puntajes_total(JUGADORES)
    imagen_generica()
    label.configure(text=f'{total[0][0].nombre} es el ganador con {total[0][1]} puntos.')

        


# def reanudar_partida(numero_partida:int):
#     '''
#     Toma como parametro la ultima partida y la retoma de donde quedó
#     '''
#     llamado_BD = 'jugadores de la BD de esa partida' #Iterar para crear instancias de la clase jugador
#     JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
#     for _,jugador in JUGADORES.items():
#         print(f'\nJugador #{_}: {jugador.nombre}\nPuntaje parcial:\n')
#         headers = ['# Turno', '# Tiro', 'Escalera', 'Full', 'Poker', 'Generala', 'Generala doble', '1', '2', '3', '4', '5', '6']
#         print(tabulate(jugador.puntaje[:-1], headers=headers, tablefmt="rst"))
#     ronda = JUGADORES[1].puntaje[0]
#     for turno in range(ronda,12):
#         print(f'\n*** Ronda numero {turno} ***\n')
#         for numero, jugador in JUGADORES.items():
#             print(f'\nEs el turno del jugador #{numero}: {jugador.nombre}')
#             dados_elegidos = tirada([],dados_elegidos, dice, entrada, boton_submit, root, label, img_dados_generico)
#             menu_despues_de_tirada(dados_elegidos,jugador.puntaje[1],jugador)
#             jugador.puntaje[0] += 1
#             if pregunta_continuar(numero_partida):
#                 pass
#     sumar_puntajes(JUGADORES)
#     volver_a_jugar = input(f'\nDesea volver a jugar?\nPresione 1 para volver a jugar o ENTER para finalizar\n')
#     if volver_a_jugar == '1':
#         nueva_partida()
#     else:
#         cerrar_partida()

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