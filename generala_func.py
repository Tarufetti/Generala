import random
from collections import defaultdict

dados_dic = {1:'       \n|       |\n|   *   |\n|       |\n       ', 
            2:'       \n| *     |\n|       |\n|     * |\n       ',
            3:'       \n|   *   |\n|   *   |\n|   *   |\n       ',
            4:'       \n| *   * |\n|       |\n| *   * |\n       ',
            5:'       \n| *   * |\n|   *   |\n| *   * |\n       ',
            6:'       \n| *   * |\n| *   * |\n| *   * |\n       '}
jugadas_grandes = {'escalera':20, 'full':30, 'poker':40, 'generala':50, 'generala_doble':100}

def tirada(dados_elegidos):
    dados_tirados = []
    _ = input('Presione una tecla para arrojar los dados: ')
    for _ in range((5-len(dados_elegidos))):
        dados_tirados.append(random.randint(1,6))
    dados_elegidos.extend(dados_tirados)
    dados_elegidos.sort()
    print(dados_elegidos)
    print(dados_dic[dados_elegidos[0]],dados_dic[dados_elegidos[1]],dados_dic[dados_elegidos[2]],dados_dic[dados_elegidos[3]],dados_dic[dados_elegidos[4]])
    return dados_elegidos


def check_jugadas_grandes(dados_elegidos,nro_tiro):
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
            print('GENERALA SERVIDA!!!! Ganaste el juego!')
            #agregar fin del juego en este momento?
    return jugadas
    
def check_jugadas_chicas(dados_elegidos):
    jugadas_chicas_dic = defaultdict(int)
    for i in range(1,7):
            jugadas_chicas_dic[f'{i}'] = i * dados_elegidos.count(i)
    lista_jugadas_chicas = []
    for k,v in jugadas_chicas_dic.items():
        if v != 0:
            lista_jugadas_chicas.append(f'{v} al {k}')
    return lista_jugadas_chicas

def menu_despues_de_tirada(dados_elegidos):
    grandes = check_jugadas_grandes(dados_elegidos, 1)
    chicas = check_jugadas_chicas(dados_elegidos)
    grandes.extend(chicas)
    for i,jug in enumerate(grandes, start=1):
        print(f'{i}- {jug}')