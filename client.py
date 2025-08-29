#####################################################
# Camada Física da Computação
# Carareto
# 11/08/2022
# Aplicação - CLIENTE
####################################################

from enlace import *
import time
import struct
import random 

serialName = "COM3"  # Windows (verifique se esta é a porta COM correta para o cliente)

# Lista de números que podem ser enviados
listanum = [
    1037.0000, -1.43567, 12.3456, 987.654, -500.0, 
    1.23e5, 45.4500, 200.123, -19.99, 88.88,
    -1000.5, 7.0, 3.14159, 2.71828, -0.0001
]

def main():
    
    try:
        print("Iniciou o main do CLIENTE")
        # Cria uma instância da classe enlace
        com1 = enlace(serialName)
        
        # Ativa a comunicação. Inicia os threads e a comunicação serial 
        com1.enable()
        print("Abriu a comunicação com o servidor")
        
        # 1. ENVIAR O BYTE DE SACRIFÍCIO
        print("Enviando byte de sacrifício...")
        time.sleep(.2)
        com1.sendData(b'\x00')
        time.sleep(1)
        print("Byte de sacrifício enviado.")

        # 2. ENVIAR A QUANTIDADE DE NÚMEROS
        nAleatorio = random.randint(5, 15)
        print(f"Serão enviados {nAleatorio} números.")
        # Envia a quantidade como um único byte
        quantidade_bytes = nAleatorio.to_bytes(1, byteorder="big")
        com1.sendData(quantidade_bytes)
        time.sleep(0.1)

        # 3. ENVIAR OS NÚMEROS
        numeros_enviados = []
        for i in range(nAleatorio):
            numero = listanum[i]
            numeros_enviados.append(numero)
            
            print(f"Enviando número [{i+1}/{nAleatorio}]: {numero}")
            # Empacota o float em 4 bytes (padrão IEEE 754) e envia
            com1.sendData(struct.pack(">f", numero))
            time.sleep(0.05) # Delay entre envios para não sobrecarregar o buffer
        
        print("\nTodos os números foram enviados. Aguardando a soma do servidor...")

        rx, nRx = com1.getData(4)
        soma_servidor = struct.unpack(">f", rx)[0]
        print(soma_servidor)

    except Exception as erro:
        print("Ops! Ocorreu um erro no cliente:-\\")
        print(erro)
    finally:
        # Garante que a comunicação será encerrada mesmo que ocorra um erro
        print("Encerrando a comunicação do cliente.")
        com1.disable()

if __name__ == "__main__":
    main()
