#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação - SERVIDOR
####################################################

from enlace import *
import time
import struct

# O nome da porta serial deve ser o mesmo usado no client
serialName = "COM7"  # Windows

def main():
    try:
        print("Iniciou o main do SERVIDOR")
        # Cria uma instância da classe enlace
        com1 = enlace(serialName)
        
        # Ativa a comunicação. Inicia os threads e a comunicação serial
        com1.enable()
        print("Servidor pronto. Aguardando conexão...")

       
        # O servidor deve ficar aguardando o byte de sacrifício do cliente
        print("Esperando 1 byte de sacrifício")
        rxBuffer, nRx = com1.getData(1)
        com1.rx.clearBuffer()
        time.sleep(0.1)
        print("Byte de sacrifício recebido e descartado.")

       
        # O próximo byte enviado pelo cliente informa quantos números serão transmitidos
        print("Aguardando a quantidade de comandos...")
        rxBuffer, nRx = com1.getData(1)
        # Converte os 4 bytes recebidos (float) para um número inteiro
        num_comandos = int.from_bytes(rxBuffer,"big")
        print(f"O cliente enviará {num_comandos} número(s).")
        
       
        numeros_recebidos = []
        soma_total = 0.0

        
        # Loop para receber cada número individualmente
        for i in range(num_comandos):
            # Cada float  ocupa 4 bytes
            rxBuffer, nRx = com1.getData(4)
            # Desempacota os 4 bytes para obter o número float
            
            numero_float = struct.unpack(">f", rxBuffer)[0]
            
            print(f"Recebido [{i+1}/{num_comandos}]: {numero_float}")
            
            numeros_recebidos.append(numero_float)
            soma_total += numero_float
        
        print("\nTodos os números foram recebidos com sucesso!")
        print(f"Lista de números recebidos: {numeros_recebidos}")
        print(f"Soma total: {soma_total:.6f}")

       
        print("Enviando a soma de volta para o cliente...")
        # Empacota a soma em 4 bytes e envia
        soma_bytes = struct.pack(">f", soma_total)
        com1.sendData(soma_bytes)
        time.sleep(0.2)
        
        print("Soma enviada.")

    except Exception as erro:
        print("Ops! Ocorreu um erro no servidor:-\\")
        print(erro)
    finally:
        
        print("Encerrando a comunicação do servidor.")
        com1.disable()

if __name__ == "__main__":
    main()