import os
from enlace import *
from math import ceil
import crcmod

class Package:
    contador_indice = 0
    image_bytes = bytearray()

    def __init__(self, tipo: int, file_path: str='', status:int=0, msg:int=0):
        # Inicializa variáveis de classe para cada novo arquivo
        if file_path:
            Package.image_bytes = self.image_to_bytes(file_path)
            
        else:
            Package.image_bytes = bytearray([0]*100)

        self.tipo = tipo
        self.file_size = len(Package.image_bytes)
        self.payload = bytearray()
        self.msg=msg
        self.status=status
        # O header e EOP serão criados por pacote, não no construtor

    def cria_header(self, checksum, status=0, msg = 0):
        h1 = self.tipo
        h2 = self.file_size
        h3 = ceil(self.file_size / 100)
        h4 = Package.contador_indice
        h5 = self.status
        h6 = self.msg
        file_size_bytes = self.file_size.to_bytes(4, byteorder='big')
        h7, h8, h9, h10 = file_size_bytes
        valor_checksum = checksum & 0xFFFF  # Garante que o checksum caiba em 2 bytes
        h11 = (valor_checksum >> 8) & 0xFF  # Byte
        h12 = valor_checksum & 0xFF  # Byte
        header = [h1, h2, h3, h4, h5, h6, h7, h8, h9, h10, h11, h12]
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
            crc = crcmod.mkCrcFun(0x11021)
            checksum = crc(payload)
            print(f"Checksum do payload {i+1}: {checksum}")
            pacote = self.cria_header(checksum) + payload + eop
            lista_pacotes.append(pacote)
        Package.contador_indice = 0
        Package.image_bytes = bytearray()
        return lista_pacotes
