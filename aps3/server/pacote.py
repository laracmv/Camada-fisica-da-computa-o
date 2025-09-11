import os
from enlace import *
from math import ceil


class Package:
    contador_indice = 0
    image_bytes = bytearray()

    def __init__(
        self, com1: enlace,
        file_path: str
    ):
        # somado toda vez que a classe for criada.
        Package.contador_indice += 1
        Package.image_bytes = self.image_to_bytes(file_path)
        self.file_size = len(Package.image_bytes)
        self.payload = bytearray()
        self.header = self.cria_header()
        if Package.contador_indice != self.header[2]:
            self.eop = bytearray((0, 0, 0))
        else:
            self.eop = bytearray((69, 69, 69))

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
        return _bytes

    def image_to_bytes(self, path):
        with open(path) as img:
            content = bytearray(img.read(), encoding='utf-8')
        return content

    def cria_payload(self):
        tamanho = self.header[5] + self.header[6]

        if self.header[3] == 4:
            self.payload = Package.image_bytes[:30]
            self.payload[30:100] = bytes(0)
        else:
            if tamanho > 100:
                self.payload = Package.image_bytes[:100]
                Package.image_bytes = Package.image_bytes[100:]

    def cria_pacote(self):
        n_payloads = self.header[3]
        lista_pacotes = []
        for i in range(n_payloads):
            self.cria_payload()
            header_bytes = bytearray(self.header)
            pacote = header_bytes + self.payload + self.eop
            lista_pacotes.append(pacote)
            print(len(pacote))
            Package.contador_indice += 1
        return lista_pacotes
