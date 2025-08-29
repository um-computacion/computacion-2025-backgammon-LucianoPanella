#Revisar y completar

class pieza:
    def __init__(self, color: str):
        self.__color__ = color
    
    def __str__(self):
        return f"Pieza de color: {self.__color__}"
