import os
from enlace import *
from math import ceil


class Package:
    contador_indice = 0 

    def __init__(
        self, com1: enlace,
        mensagem=''
        ):
        Package.contador_indice +=1 #somado toda vez que a classe for criada.
        self.msg = mensagem
        self.payload = []
        self.eop = bytearray((69, 69, 69))
        self.file_size = 0
        self.content = bytes(0)
        self.header = self.cria_header()
        pass
    
    def cria_header(self):
        h2 = self.file_size # tamanho da mensagem
        h3 = ceil(self.file_size / 100) # numero de pacotes

        h4 = Package.contador_indice #indice que esta sendo iterado

        h5 = 0
        if self.file_size > 255:
            h6 = 255
        else:
            h6 = self.file_size
        
        h7 = self.file_size - 255
        if h7 < 0:
            h7 = 0
        
        _bytes = [1, h2, h3, h4, h5, h6, h7]
        
        pass