#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
from struct import unpack, pack
import time
import numpy as np
# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

# use uma das 3 opcoes para atribuir à variável a porta usada
serialName = "/dev/ttyUSB0"           # Ubuntu (variacao de)
# serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
# serialName = "COM4"                  # Windows(variacao de)  detectar sua porta e substituir aqui


def main():
    try:
        print("Iniciou o main")
        # declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        # para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        recebeu = False
        

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        # ---------------- BIT DE SACRIFÍCIO ----------------
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(.5)
        # ---------------------------------------------------

        msg: str = "aoba"

        bytes_msg = msg.encode(encoding='utf-8')
        len_msg = pack('<f', len(msg))
        print(len(bytes_msg))
        
        time.sleep(.3)
        com1.sendData(len_msg)
        time.sleep(.1)
        com1.sendData(bytes_msg)
        print("Enviou mensagem")
        time.sleep(.1)
        hora_envio = time.time()
        rx_buffer = None
        
        print("Esperando")
        while time.time() - hora_envio < 3:
            nRx = com1.rx.getBufferLen()
            if nRx:
                rx_buffer = com1.getData(1)[0]
                break
        
        if not rx_buffer:
            print("Demorou muito para receber arquivos")

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()