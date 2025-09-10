#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação
####################################################


# esta é a camada superior, de aplicação do seu software de comunicação serial UART.
# para acompanhar a execução e identificar erros, construa prints ao longo do código!


from enlace import *
import time
from utils import manda_arquivo
from pacote import Package

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

        # ---------------- BYTE DE SACRIFÍCIO ----------------
        time.sleep(.2)
        com1.sendData(b'00')
        print('mandou byte')
        time.sleep(1)
        # ---------------------------------------------------

        msg: str = "aoba"

        bytes_msg = msg.encode(encoding='utf-8')
        len_msg = len(msg).to_bytes(4)
        print(len(bytes_msg))
        
        time.sleep(.3)
        com1.sendData(len_msg)
        time.sleep(.1)
        com1.sendData(bytes_msg)
        time.sleep(.1)
        hora_envio = time.time()
        rx_buffer = None
        
        print("Esperando")
        while time.time() - hora_envio < 3:
            nRx = com1.rx.getBufferLen()
            if nRx:
                rx_buffer = com1.getData(4)[0]
                break
        
        if not rx_buffer:
            print("Demorou muito para receber arquivos")
        else:
            rx_int = int.from_bytes(rx_buffer)
            print(rx_int)
            print("Arquivos disponíveis")
            
            for i in range(rx_int):
                    arq = com1.getData(11)[0]
                    print(arq.decode())
            
            while True:
                arq_escolhido = input("Escolha um deles: ")
                
                bytes_arq = arq_escolhido.encode()
                len_arq = len(arq_escolhido).to_bytes(4)
                time.sleep(.3)
                com1.sendData(len_arq)
                time.sleep(.1)
                com1.sendData(bytes_arq)
                time.sleep(.3)
                print("mandou arquivo")
                
                if arq_escolhido == 'nao':
                    break
                
                size_resp = com1.getData(4)[0]
                time.sleep(.1)
                size_resp = int.from_bytes(size_resp)
                resp = com1.getData(size_resp)[0]
                time.sleep(.1)
            
            
        print("Acabou")

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()