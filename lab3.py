abc = ' !"#$%&\'()*+,-./0123456789:;<=>?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\\]^_`abcdefghijklmnopqrstuvwxyz{|}~'
from Tkinter import *
from timeit import default_timer as timer
# Funcion de Encriptacion
# Entrada: Mensaje a encriptar y llave de encriptacion
# Salida: Mensaje Encriptado
# Nota: esta funcion se puede utilizar para el procesod e desencriptacion
def encript(message, key):
    message_encripted = ''
    for i in range(len(message)):
        mess_char = ord(message[i])
        key_char = ord(key[i%len(key)])
        char_encripted = chr(mess_char ^ key_char)
        message_encripted += char_encripted
    return message_encripted


# Funcion que intercambia la posicion entre pares de un arrglo
# Si la funcion es impar se mantiene la posicion del caracter central
# Entrada: Arreglo de cualquier tipo
# Salida: Arreglo con las posiciones modificadas
# Ejemplo:
# Caso par:
#   Entrada = [1,2,3,4,5,6]
#   Salida = [2,1,4,3,6,5]
# Caso impar 1:
#   Entrada = [1,2,3,4,5,6,7]
#   Salida = [2,1,5,4,3,7,6]
# Caso impar 2:
#   Entrada = [1,2,3,4,5]
#   Salida = [2,1,3,5,4]
def swap(bloq):
    # Se verifica la paridad del mensaje, si es impar el ultimo caracter se mantiene en su posicion
    if(len(bloq)%2==0):
        for i in range(0, len(bloq)/2):
            aux = bloq[2*i]
            bloq[2*i] = bloq[2*i+1]
            bloq[2*i+1] = aux
    else:
        centro = int(round(len(bloq))/2)
        if(centro%2!=0):
            for i in range(0, int(round(len(bloq)/2))):
                if(2*i+1<centro):
                    aux = bloq[2*i]
                    bloq[2*i] = bloq[2*i+1]
                    bloq[2*i+1] = aux
                elif(2*i+1==centro):
                    aux = bloq[2*i]
                    bloq[2*i] = bloq[2*i+2]
                    bloq[2*i+2] = aux
                else:
                    aux = bloq[2*i+1]
                    bloq[2*i+1] = bloq[2*i+2]
                    bloq[2*i+2] = aux

        else:
            for i in range(0, int(round(len(bloq)/2))):
                if(i<(centro/2)):
                    aux = bloq[2*i]
                    bloq[2*i] = bloq[2*i+1]
                    bloq[2*i+1] = aux
                else:
                    aux = bloq[2*i+1]
                    bloq[2*i+1] = bloq[2*i+2]
                    bloq[2*i+2] = aux
    return bloq


def alg_encript(message, key, block_size):
    blocks = []
    # Se verifica que el largo del mensaje sea multiplo del tamano del bloque
    # De no ser asi, se rellenara con la ultima letra del mensaje hasta tener
    # un largo a un multiplo del tamano de bloque
    if(len(message)%block_size!=0):
        char = 'x'
        while(len(message)%block_size!=0):
            message += char
    # Se crean los bloques correspondientes
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]
        blocks.append(block)

    # Comienza el proceso de encriptacion de cada bloque
    encripted_blocks = []
    for i in range(len(blocks)):
        encripted_blocks.append(encript(blocks[i],key[i%len(key)]))
    # Se aplica la funcion "swap" para intercambiar las posiciones de cada bloque
    
    encripted_blocks = swap(encripted_blocks)
    
    encripted_chars = []
    for block in encripted_blocks:
        for char in block:
            encripted_chars.append(char)
    

    for i, char_1 in enumerate(encripted_chars):
            for j, char_2 in enumerate(encripted_chars):
                if(i != j):
                    encripted_chars[j] = chr((ord(char_1)+ord(char_2))%127)

    encripted_message = ''
    for char in encripted_chars:
        encripted_message += char
    return encripted_message

def alg_desencript(encripted_message, key, block_size):
    encripted_chars = []
    for char in encripted_message:
        encripted_chars.append(char)
    
    encripted_chars = list(reversed(encripted_chars))
    
    for i, char_1 in enumerate(encripted_chars):
            for j, char_2 in enumerate(encripted_chars):
                if(i != j):
                    encripted_chars[j] = chr((ord(char_2)-ord(char_1))%127)
    encripted_chars = list(reversed(encripted_chars))
    
    encripted_blocks = []
    for i in range(0, len(encripted_chars), block_size):
        block = encripted_chars[i:i+block_size]
        encripted_blocks.append(''.join(block))
    encripted_blocks = swap(encripted_blocks)

    desencripted_blocks = []
    for i in range(len(encripted_blocks)):
        desencripted_blocks.append(encript(encripted_blocks[i],key[i%len(key)]))
    
    desencripted_message = ''
    for block in desencripted_blocks:
        desencripted_message += block
    return desencripted_message

def blocksToString(blocks):
    text = ''
    for i in range(len(blocks)):
        text = text + blocks[i]
    return text
def mac(message, key, block_size):
    blocks = []
    # Se verifica que el largo del mensaje sea multiplo del tamano del bloque
    # De no ser asi, se rellenara con x's el mensaje hasta tener
    # un largo a un multiplo del tamano de bloque
    if(len(message)%block_size!=0):
        char = 'x'
        while(len(message)%block_size!=0):
            message += char
    # Se crean los bloques correspondientes
    for i in range(0, len(message), block_size):
        block = message[i:i+block_size]
        blocks.append(block)

    # Comienza el proceso de encriptacion de cada bloque
    encripted_blocks = []
    for i in range(len(blocks)):
        if(i==0):
            encripted_blocks.append(encript(blocks[i],key[i%len(key)]))
        else:
            prev_encript_block = encripted_blocks[i-1]
            aux = encript(block[i],prev_encript_block)
            encripted_blocks.append(encript(aux,key[i%len(key)]))
        
    # Se aplica la funcion "swap" para intercambiar las posiciones de cada bloque
    
    encripted_blocks = swap(encripted_blocks)
    
    encripted_chars = []
    for block in encripted_blocks:
        for char in block:
            encripted_chars.append(char)
    

    for i, char_1 in enumerate(encripted_chars):
            for j, char_2 in enumerate(encripted_chars):
                if(i != j):
                    encripted_chars[j] = chr((ord(char_1)+ord(char_2))%127)

    encripted_message = ''
    for char in encripted_chars:
        encripted_message += char
    return encripted_message
flag = TRUE
while flag:
    print("################################################")
    print("###############  Inicio programa  ##############")
    print("################################################")
    print("Ingrese el tamano del bloque: ")
    block_size = int(raw_input())
    print("Ingrese el tamano de MAC: ")
    mac_size = int(raw_input())
    print("Ingrese texto a encriptar: ")
    text = raw_input()
    start_enc = timer()
    result = alg_encript(text, 'q1w2e3r4t5',block_size)
    end_enc = timer()
    print(text)
    mac_message = mac(text, 'q1w2e3r4t5', mac_size)
    time_enc = end_enc - start_enc
    toSend = [mac_message,result]
    print("Mensaje cifrado: " + result+"\nMac enviado: "+mac_message)
    print("Tiempo: " + str(time_enc))
    mac_rec = toSend[0]
    result = toSend[1]
    start_denc = timer()
    result = alg_desencript(result,'q1w2e3r4t5',block_size)
    end_denc = timer()
    un_mac_message = mac(result, 'q1w2e3r4t5', mac_size)
    time_denc = end_denc - start_denc
    print("Mensaje descifrado: " + result + "\nMac recibido " + mac_rec+ "\nMac mensaje " + un_mac_message)
    print("Tiempo: "+ str(time_denc))
    print("Desea continuar?")
    print("1.- Si")
    print("2.- No")
    opc = input()
    if(opc == 2):
        break