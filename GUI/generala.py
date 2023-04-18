import customtkinter as ctk
import CTkMessagebox
from PIL import Image
import os

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
boton_submit = ctk.CTkButton(master=root,text='Tirar dados!', fg_color="red")
boton_submit.grid(row=3, column=7, padx=(20, 20), pady=(20, 20), sticky="nsew")

#Creacion de las imagenes
dice = []
dice_relx = 0.20
for i in range(1,6):
    img = ctk.CTkImage(Image.open(f'{cwd}/resources/dice{i}.png'),size=(100,100))
    img_label = ctk.CTkLabel(master=root,text='', image=img)
    img_label.place(relx=dice_relx, rely = 0.15)
    dice_relx += 0.15
    dice.append(img_label)


#Creacion de los checkboxes
checkboxes = []
check_relx = 0.25
for i in range(1,6):
    checkbox = ctk.CTkCheckBox(root, text=f'{i}')
    checkbox.place(relx= check_relx, rely= 0.5)
    check_relx += 0.15
    checkboxes.append(checkbox)


root.mainloop()