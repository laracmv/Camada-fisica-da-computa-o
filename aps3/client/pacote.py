import os
from enlace import *
from math import ceil


class Package:
    def __init__(
        self, com1: enlace,
        mensagem=''
        ):
        
        self.msg = mensagem
        self.payload = []
        self.eop = bytearray((69, 69, 69))
        self.file_size = 0
        self.content = bytes(0)
        pass
    
    def cria_header(self):
        h2 = self.file_size # tamanho da mensagem
        h3 = ceil(self.file_size / 100) # numero de pacotes
        
        pass