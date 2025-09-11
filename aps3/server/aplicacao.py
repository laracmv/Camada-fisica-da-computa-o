#####################################################
# Camada Física da Computação
#Carareto
#11/08/2022
#Aplicação
####################################################


#esta é a camada superior, de aplicação do seu software de comunicação serial UART.
#para acompanhar a execução e identificar erros, construa prints ao longo do código! 


from enlace import *
import time
import numpy as np
from pacote import Package

# voce deverá descomentar e configurar a porta com através da qual ira fazer comunicaçao
#   para saber a sua porta, execute no terminal :
#   python -m serial.tools.list_ports
# se estiver usando windows, o gerenciador de dispositivos informa a porta

#use uma das 3 opcoes para atribuir à variável a porta usada
#serialName = "/dev/ttyACM0"           # Ubuntu (variacao de)
#serialName = "/dev/tty.usbmodem1411" # Mac    (variacao de)
serialName = "COM5"                  # Windows(variacao de)  detectar sua porta e substituir aqui


def main():
    try:
        print("Iniciou o main")
        #declaramos um objeto do tipo enlace com o nome "com". Essa é a camada inferior à aplicação. Observe que um parametro
        #para declarar esse objeto é o nome da porta.
        com1 = enlace(serialName)
        
        nome_arquivos = []
        arquivos_desejados = []
    
        # Ativa comunicacao. Inicia os threads e a comunicação seiral 
        com1.enable()
        #Se chegamos até aqui, a comunicação foi aberta com sucesso. Faça um print para informar.
        print("Abriu a comunicação")
        
        print("esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(.1)
        print("1 byte recebido")
        
        rxBuffer, nRx = com1.getData(4)
        print(rxBuffer)
        len_frase = int.from_bytes(rxBuffer)
        time.sleep(0.1)
        
        print("Recebendo handshake")
        rxBuffer, nRx = com1.getData(len_frase)
        string = rxBuffer.decode('utf-8')
        print(string)
        print("Frase recebida")
        time.sleep(.1)
        
        n_arquivos = 4
        com1.sendData(n_arquivos.to_bytes(4))
        time.sleep(.1)
        print("Enviando nomes de arquivos")
        
        for i in range(4):
            nome_arquivo = f"Fodase{i+1}.txt"
            nome_arquivos.append(nome_arquivo)
            nome_arquivo_bytes = nome_arquivo.encode(encoding='utf-8')
            com1.sendData(nome_arquivo_bytes)
            time.sleep(.1)
        
        print("Nomes enviados")
         
        msg = f"Gostaria de qual arquivo? "
        len_msg = len(msg)
        com1.sendData(len_msg.to_bytes(4))
        time.sleep(.1)
        com1.sendData(msg.encode('utf-8'))
        time.sleep(.1)
        
        print("Esperando resposta do cliente")
        
         # Esperar resposta do cliente
        len_resposta = com1.getData(4)[0]
        len_resposta = int.from_bytes(len_resposta)
        time.sleep(.1)
        
        resposta = com1.getData(len_resposta)
        resposta = resposta[0].decode('utf-8')
        
        while resposta != "nao" and resposta != "":
            if resposta in nome_arquivos:
                print(f"Cliente escolheu o arquivo: {resposta}")
                arquivos_desejados.append("C:\\Users\\lorag\\OneDrive - Insper - Institudo de Ensino e Pesquisa\\VSC\\Camadas\\Camada-fisica-da-computa-o\\aps3\\Arquivos\\" + resposta)
                msg = f"arquivo {resposta} disponivel, quer adicionar mais algum? "
                len_msg = len(msg)
                com1.sendData(len_msg.to_bytes(4))
                time.sleep(.1)
                com1.sendData(msg.encode('utf-8'))
            else:
                msg = f"arquivo {resposta} nao disponivel, quer adicionar mais algum? "
                len_msg = len(msg)
                com1.sendData(len_msg.to_bytes(4))
                time.sleep(.1)
                com1.sendData(msg.encode('utf-8'))
            time.sleep(.1)
            
            len_resposta = com1.getData(4)[0]
            len_resposta = int.from_bytes(len_resposta)
            time.sleep(.1)
            resposta = com1.getData(len_resposta)
            resposta = resposta[0].decode('utf-8')
            print("Resposta do cliente:", resposta)
            time.sleep(.1)     
        
        print("Arquivos desejados:", arquivos_desejados)
        
        for arquivo in arquivos_desejados:
            print(f"Enviando arquivo: {arquivo}")
            pacotes = Package(com1, arquivo).cria_pacote()
            print("Arquivo lido")
            for pacote in pacotes:
                print(pacote)
                com1.sendData(pacote)
                print("Enviando pacote...")
                time.sleep(0.1)
            time.sleep(0.1)
            print("Arquivo enviado")

        # print("Quantidade de elementos a serem recebidos:", len_num)
        # print("Byte de sacrificio recebido")
        
        # total = 0

        # for i in range(len_num):
        #     rxBuffer, nRx = com1.getData(4)
        #     if nRx > 0:
        #         float_value = struct.unpack('<f', rxBuffer)[0]
        #         print(float_value)
        #         total += float_value
        #         ultimo_recebimento = time.time()
        #     time.sleep(0.01)
        
        # print("Encerrando recebimento")

        # # Converter total para bytes e enviar
        # total_bytes = struct.pack('<f', total)
        # com1.sendData(total_bytes)
        # print("Total enviado:", total)

        print("-------------------------")
        print("Comunicação encerrada")
        print("-------------------------")
        com1.disable()
        
    except Exception as erro:
        print("ops! :-\\")
        print(erro)
        com1.disable()
        

    #so roda o main quando for executado do terminal ... se for chamado dentro de outro modulo nao roda
if __name__ == "__main__":
    main()