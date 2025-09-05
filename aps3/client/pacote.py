from enlace import *

class Package:
    def __init__(self, pacote):
        self.pacote = pacote
        self.h1 = pacote[0]

        # caso seja 0 será comunicacao
        if self.h1 == 0:
            self.comunicacao()
        else:
            self.transmissao()

    def comunicacao(self):
        self.h2 = self.pacote[1] #tamanho mensagem
        # self.h3 = self.pacote[2]
        self.h12 = self.pacote[11] #status mensagem
    
    def transmissao(self):
        self.h2 = self.pacote[1] #tamanho mensagem
        self.h3 = self.pacote[2] #numero de pacotes
        self.h4 = self.pacote[3] # indice
        self.h5 = self.pacote[4] #mensagem de erro