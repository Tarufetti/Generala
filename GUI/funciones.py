import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from collections import defaultdict

def submit(entrada, entry):
    entrada.set(entry.get())

def nueva_partida(root, entrada, entry, boton_submit, boton_n_partida, boton_r_partida, boton_puntajes_altos):
    '''
    Comienza nueva partida.
    '''
    #modifica la pantalla principal
    boton_n_partida.place_forget()
    boton_r_partida.place_forget()
    boton_puntajes_altos.place_forget()
    boton_submit.configure(text='Enter!', fg_color='blue',state='normal')
    
    #comienza la ejecucion del juego
    seleccion_jugadores = ctk.CTkLabel(master=root, text='Selecciona la cantidad de jugadores: ', font=('roboto',24))
    seleccion_jugadores.place(relx=0.20, rely=0.30)
    boton_submit.wait_variable(entrada)
    cant_jugadores = entry.get()
    if not cant_jugadores.isdigit() or int(cant_jugadores) > 10:
        CTkMessagebox(title='Generala', icon = 'cancel', message = 'Seleccione la cantidad de jugadores (1-10) usando NUMEROS', option_1 = 'OK', button_color='blue')
    JUGADORES = defaultdict(lambda: 'No existe dicho jugador')
    numero_partida = 1#recolectar de BD el numero, puse 1 para probar
    
    
    #******* modificar a partir de aca ******
    
    for i in range(1, int(cant_jugadores)+1):
        x = input(f'\nElige el nombre del jugador {i}: ')
        JUGADORES[i] = Jugador(x,numero_partida)
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