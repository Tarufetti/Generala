import customtkinter as ctk
import CTkMessagebox
from PIL import Image
import os
import funciones

#Creacion del cuadro principal de la GUI
root = ctk.CTk()
root.title('Generala')
cwd = os.getcwd()
root.iconbitmap(f'{cwd}\\resources\\icono.ico')
root.geometry('950x600')
root.resizable(False,False)
ctk.set_appearance_mode('system')


#Configuracion de un grid
root.grid_columnconfigure(1, weight=1)
root.grid_columnconfigure((2, 3), weight=0)
root.grid_rowconfigure((0, 1, 2), weight=1)

#Creacion de los cuadros interiores de la GUI
frame_izq = ctk.CTkFrame(master=root, width=170)
frame_izq.grid(row=0, column=0, rowspan=4, sticky="nsew")

#Creacion del cuadro de entrada y boton submit principal
entry = ctk.CTkEntry(root)
entry.grid(row=3, column=1, columnspan=6, padx=(20, 0), pady=(20, 20), sticky="nsew")
boton_submit = ctk.CTkButton(master=root,text='', fg_color="grey", state='dissabled')
boton_submit.grid(row=3, column=7, padx=(20, 20), pady=(20, 20), sticky="nsew")

#Consulta a la BBDD por el numero de la ultima partida
numero_partida = 1

#Creacion de las imagenes
dice = []
dice_relx = 0.20 # incrementa de a 0.15 para mantener simetria
dice_rely = 0.15
for i in range(1,6):
    img = ctk.CTkImage(Image.open(f'{cwd}/resources/dice{i}.png'),size=(100,100))
    img_label = ctk.CTkLabel(master=root,text='', image=img)
    dice.append(img_label)

#Creacion de los checkboxes
checkboxes = []
check_relx = 0.25 #incrementa de a 0.15
check_rely = 0.45
for i in range(1,6):
    checkbox = ctk.CTkCheckBox(root, text=f'{i}')
    checkboxes.append(checkbox)

bienvenido = ctk.CTkLabel(root, text='Bienvenido a la Generala!', font=('roboto',60, 'bold'))
bienvenido.place(relx= 0.20, rely=0.10)

boton_n_partida = ctk.CTkButton(root, width=200, height=60, text='Nueva Partida', font=('roboto', 20), fg_color='blue', command=lambda: funciones.nueva_partida())
boton_n_partida.place(relx= 0.48, rely=0.30)
boton_r_partida = ctk.CTkButton(root, width=200, height=60, text='Reanudar Partida', font=('roboto', 20), fg_color='blue', command=lambda: funciones.reanudar_partida(numero_partida))
boton_r_partida.place(relx= 0.48, rely=0.45)
boton_puntajes_altos = ctk.CTkButton(root, width=200, height=60, text='Puntajes mas altos', font=('roboto', 20), fg_color='blue',command=lambda: funciones.puntajes_altos(root,bienvenido, boton_n_partida, boton_r_partida, boton_puntajes_altos))
boton_puntajes_altos.place(relx= 0.48, rely=0.60)








if __name__ == '__main__':
    root.mainloop()