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

def separa_mensagem(enlace: enlace, file_content: str):
    byte_content = bytearray(file_content)
    
    payloads = []
    num_payloads = ceil(byte_content / 100)