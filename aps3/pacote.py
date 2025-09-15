import os
from client.enlace import *
from math import ceil


class Package:
    contador_indice = 0
    image_bytes = 0

    def __init__(
        self, com1: enlace,
        file_path: str
    ):
        # somado toda vez que a classe for criada.
        Package.contador_indice += 1
        Package.image_bytes = self.image_to_bytes(file_path)
        self.payload = None
        self.header = self.cria_header()
        if Package.contador_indice != self.header[2]:
            self.eop = bytearray((0, 0, 0))
        else:
            self.eop = bytearray((69, 69, 69))

        self.file_size = len(self.image_bytes)
        pass

    def cria_header(self):
        h2 = self.file_size  # tamanho da mensagem
        h3 = ceil(self.file_size / 100)  # numero de pacotes

        h4 = Package.contador_indice  # indice que esta sendo iterado'

        h5 = 0
        if self.file_size > 255:
            h6 = 255
        else:
            h6 = self.file_size

        h7 = self.file_size - 255
        if h7 < 0:
            h7 = 0

        _bytes = [1, h2, h3, h4, h5, h6, h7, 0, 0, 0, 0, 0]

        pass

    def image_to_bytes(self, path):
        with open(path) as img:
            content = bytearray(img.read(), encoding='utf-8')
        return content

    def cria_payload(self):
        tamanho = self.header[5] + self.header[6]

        if tamanho >= 100:
            self.payload = Package.image_bytes[:100]
            Package.image_bytes = Package.image_bytes[100:]
        else:
            self.payload = Package.image_bytes[:]
            Package.image_bytes = []
        pass

    def cria_pacote(self):
        n_payloads = self.header[3]
        lista_pacotes = []
        for i in range(n_payloads):
            self.cria_payload()
            pacote = self.header + self.payload + self.eop
            lista_pacotes.append(pacote)
            Package.contador_indice += 1
        return lista_pacotes
