from datetime import datetime

def escreve_log(operacao, tipo_msg, tamanho, pacote=None, total_pacotes=None, crc=None, log_path="server\log\log.txt"):
    agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-3]
    linha = f"{agora} / {operacao} / {tipo_msg} / {tamanho}"
    if pacote is not None:
        linha += f" / {pacote}"
    if total_pacotes is not None:
        linha += f" / {total_pacotes}"
    if crc is not None:
        linha += f" / {crc:04X}"
    with open(log_path, "a") as f:
        f.write(linha + "\n")