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
from utils import decode_lista

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
        end_imagens = '/home/rafaelvb/Desktop/Engenharia/Camada-fisica-da-computa-o/aps3/client/img_recebidas'
        # PACKAGE_SIZE = 115

        # Ativa comunicacao. Inicia os threads e a comunicação seiral
        com1.enable()

        # ---------------- BYTE DE SACRIFÍCIO ----------------
        time.sleep(.2)
        com1.sendData(b'00')
        time.sleep(1)
        # ---------------------------------------------------

        msg: str = "aoba"

        bytes_msg = msg.encode(encoding='utf-8')
        len_msg = len(msg).to_bytes(4)

        time.sleep(.3)
        com1.sendData(len_msg)
        time.sleep(.1)
        com1.sendData(bytes_msg)
        time.sleep(.1)
        hora_envio = time.time()
        rx_buffer = None
        arquivos = 0

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
            print("Arquivos disponíveis")

            for i in range(rx_int):
                arq = com1.getData(8)[0]
                print(arq.decode())

            while True:
                time.sleep(.1)
                tam_msg = int.from_bytes(com1.getData(4)[0])
                time.sleep(.2)
                resp = com1.getData(tam_msg)[0]
                time.sleep(.3)
                print(resp.decode())
                arq_escolhido = input("> ")

                bytes_arq = arq_escolhido.encode()
                len_arq = len(arq_escolhido).to_bytes(4)

                time.sleep(.3)
                com1.sendData(len_arq)
                time.sleep(.2)
                com1.sendData(bytes_arq)
                time.sleep(.1)

                if arq_escolhido in ('nao', ''):
                    break
                else:
                    arquivos += 1
            
            content = bytearray()

            for j in range(arquivos):
                resposta: bytearray = com1.getData(115)[0]
                time.sleep(.3)
                print(f"Resposta: {resposta}")
                print('*'*50)
                header = resposta[2]
                indice = resposta[3]
                # while indice <= header:
                    # content.extend(resposta[12:112])
                    
                    # pacote = com1.getData(115)[0]
                    # time.sleep(.2)
                    # indice = pacote[3]
                    # print(f"Novo pacote: {pacote}")
                    # print(f'Indice do pacote: {pacote[3]}')
                    # content.extend(resposta[12:112])
                    
                    # pacote = com1.getData(115)[0]
                    # time.sleep(.2)
                    # indice = pacote[3]
                    # print(f"Novo pacote: {pacote}")
                    # print(f'Indice do pacote: {pacote[3]}')

                eop = decode_lista(resposta[-3:])
                while eop != (69, 69, 69):
                    content.extend(resposta[12:112])
                    
                    resposta = com1.getData(115)[0]
                    
                    time.sleep(.2)
                    eop = decode_lista(resposta[-3:])
                    print(f"Novo pacote: {resposta}")
                    print(f'Indice do pacote: {resposta[3]}')
                    print(eop)
                
                if eop == (69, 69, 69):
                    content.extend(resposta[12:112])
                    with open(end_imagens+f'/arquivo{j+1}.png', 'wb') as f:
                        f.write(content)

                        print(
                            f"Arquivo {j+1} salvo em {end_imagens+f'/arquivo{j+1}.png'}\n"
                        )
                    content = bytearray()

        print("Acabou")

        com1.disable()

    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()


    # so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()
