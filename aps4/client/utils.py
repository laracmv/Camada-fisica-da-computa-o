from enlace import *
import time
from struct import pack, unpack
from math import ceil
from pacote import Package

def manda_arquivo(enlace: enlace, content):
    if type(content) != bytes:
        if type(content) == str:
            bytes_content = content.encode()
        else:
            bytes_content = pack('<f', content)
    
    time.sleep(.3)
    enlace.sendData(bytes_content)
    time.sleep(.1)
    return

def imagem_para_bytes(file_path: str):
    with open(file_path) as f:
        return bytearray(f.read(), encoding='utf-8')

def decode_lista(lista_bytes):
    l = []
    for byte in lista_bytes:
        print(f"Byte: ", byte)
        l.append(byte)
    
    return tuple(l)