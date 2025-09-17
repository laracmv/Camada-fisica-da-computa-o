import os
from enlace import *
from math import ceil


class Package:
    contador_indice = 0
    image_bytes = bytearray()

    def __init__(self, file_path: str):
        # Inicializa variáveis de classe para cada novo arquivo
        Package.image_bytes = self.image_to_bytes(file_path)
        self.file_size = len(Package.image_bytes)
        self.payload = bytearray()
        # O header e EOP serão criados por pacote, não no construtor

    def cria_header(self):
        h2 = self.file_size
        h3 = ceil(self.file_size / 100)
        h4 = Package.contador_indice
        h5 = 0
        h6 = 255 if self.file_size > 255 else self.file_size
        h7 = self.file_size - 255 if self.file_size > 255 else 0
        h8 = self.file_size - 510 if self.file_size > 510 else 0
        h9 = self.file_size - 765 if self.file_size > 765 else 0
        h10 = self.file_size - 1020 if self.file_size > 1020 else 0
        h11 = self.file_size - 1275 if self.file_size > 1275 else 0
        h12 = self.file_size - 1530 if self.file_size > 1530 else 0
        header = [1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12]
        header_bytes = bytearray([b & 0xFF for b in header])
        return header_bytes

    def image_to_bytes(self, path):
        with open(path, 'rb') as img:
            content = bytearray(img.read())
        return content

    def cria_payloads(self):
        total_bytes = Package.image_bytes
        payloads = []
        while len(total_bytes) > 0:
            chunk = total_bytes[:100]
            total_bytes = total_bytes[100:]
            if len(chunk) < 100:
                chunk += b' ' * (100 - len(chunk))
            payloads.append(chunk)
        # Garante que o último payload tenha 100 bytes, mesmo se o arquivo for múltiplo de 100
        if payloads and len(payloads[-1]) < 100:
            payloads[-1] += b' ' * (100 - len(payloads[-1]))
        print(len(payloads))
        return payloads

    def cria_pacote(self):
        payloads = self.cria_payloads()
        lista_pacotes = []
        Package.contador_indice = 0
        for i, payload in enumerate(payloads):
            Package.contador_indice += 1
            # EOP: último pacote recebe (69,69,69), demais (0,0,0)
            if i == len(payloads) - 1:
                eop = bytearray((69, 69, 69))
            else:
                eop = bytearray((0, 0, 0))
            pacote = self.cria_header() + payload + eop
            lista_pacotes.append(pacote)
        Package.contador_indice = 0
        Package.image_bytes = bytearray()
        return lista_pacotes
