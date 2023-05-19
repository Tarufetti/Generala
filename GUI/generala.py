import customtkinter as ctk
from tkinter import ttk
from CTkMessagebox import CTkMessagebox
import os
import funciones

## CHEQUEAR EL TEMA DEL CIERRE DE LA APLICACION CUANDO SE ESTA EJECUTANDO UNA FUNCION
## CHEQUEAR AFTER SCRIPTS cuando se cierra la app
## AGREGAR ALGO PARA FRENAR EL CIERRE DE LA VENTANA HASTA QUE GUARDE EN BBDD

#pasar grilla a generala py, averiguar como se modifican valores
#cuando ronda pasa a 2, grilla izq tira error porque ya existe valor


#Creacion del cuadro principal de la GUI
root = ctk.CTk()
root.title('Generala')
cwd = os.getcwd()
root.iconbitmap(f'{cwd}\\resources\\icono.ico')
root.geometry('1120x600')
root.resizable(False,False)
root.protocol("WM_DELETE_WINDOW", lambda: funciones.cerrar_programa(root))
ctk.set_appearance_mode('light')


#Configuracion de un grid
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

#Creacion de los cuadros interiores de la GUI
frame_izq = ctk.CTkFrame(master=root, width=180)
label_ronda_frameizq = ctk.CTkLabel(master=frame_izq, width=60, text=f'Ronda #')
label_tiro_frameizq = ctk.CTkLabel(master=frame_izq, width=60, text=f'Tiro #')
label_jugador_frameizq = ctk.CTkLabel(master=frame_izq, width=60, text=f'jugador #')
grilla_puntajes_izq = ttk.Treeview(master=frame_izq, height=13, columns='Puntos')
grilla_puntajes_izq.column("#0",width=100, anchor='w')
grilla_puntajes_izq.column("Puntos",width=50, anchor='center')
grilla_puntajes_izq.heading("#0", text="Jugada", anchor='center')
grilla_puntajes_izq.heading("Puntos", text="Puntaje", anchor='center')
frame_der = ctk.CTkFrame(master=root, width=180)

#Creacion del cuadro de entrada y botones
entrada = ctk.StringVar()
entry = ctk.CTkEntry(root, width=750)
entry.grid(row=3, column=1, columnspan=6, padx=(20, 0), pady=(20, 20), sticky="e")
boton_submit = ctk.CTkButton(master=root,text='', fg_color="grey", state='disabled', command=lambda: funciones.submit(entrada, entry))
boton_submit.grid(row=3, column=7, padx=(20, 20), pady=(20, 20), sticky="nsew")
boton_elegir_dados =ctk.CTkButton(master=root, width=150, height=50 , text='Elegir dados', font=('roboto', 16), fg_color="blue", state='normal', command=lambda: funciones.elegir_dados())
boton_plantar = ctk.CTkButton(master=root, width=150, height=50, text='Plantar', font=('roboto', 16), fg_color="blue", state='normal', command=lambda: funciones.tachar())
#Consulta a la BBDD por el numero de la ultima partida
numero_partida = 1

#label de bienvenido al juego
bienvenido = ctk.CTkLabel(root, text='Bienvenido a la Generala!', font=('roboto',60, 'bold'))
bienvenido.place(relx= 0.20, rely=0.10)

#botones de la pantalla inicial
boton_n_partida = ctk.CTkButton(root, width=200, height=60, text='Nueva Partida', font=('roboto', 20), fg_color='blue', command=lambda: funciones.nueva_partida(*args))
boton_n_partida.place(relx= 0.48, rely=0.30)
boton_r_partida = ctk.CTkButton(root, width=200, height=60, text='Reanudar Partida', font=('roboto', 20), fg_color='blue', command=lambda: funciones.reanudar_partida(numero_partida))
boton_r_partida.place(relx= 0.48, rely=0.45)
boton_puntajes_altos = ctk.CTkButton(root, width=200, height=60, text='Puntajes mas altos', font=('roboto', 20), fg_color='blue',command=lambda: funciones.puntajes_altos(root,bienvenido, boton_n_partida, boton_r_partida, boton_puntajes_altos))
boton_puntajes_altos.place(relx= 0.48, rely=0.60)








args = [root, entrada, entry, boton_submit, boton_n_partida, boton_r_partida, boton_puntajes_altos, frame_izq, label_ronda_frameizq, label_jugador_frameizq, label_tiro_frameizq, grilla_puntajes_izq, frame_der, bienvenido, boton_elegir_dados, boton_plantar]
if __name__ == '__main__':
    root.mainloop()