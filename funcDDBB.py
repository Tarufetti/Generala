import mysql.connector
import json

base = mysql.connector.connect('graladice.sql')
c = base.cursor()

def guardar_partida(JUGADORES:dict, numero_partida:int) -> None:
    for _, jugador in JUGADORES.items():
        puntaje = json.dumps(jugador.puntaje)
        jug = (jugador.nombre, puntaje)
