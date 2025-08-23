import random 

class Dice:
    def __init__(self,valor):
        self.valor = 0

    def tirada(self):
        self.valor = random.randint(1, 6)
        return self.valor

print()