import random

class MemoriaExperiencia:
    def __init__(self, dim_max: int):
        if dim_max <= 0:
            raise ValueError("dim_max deve ser maior que zero")
        self.dim_max = dim_max
        self.memoria = []

    def actualizar(self, experiencia):
        if len(self.memoria) == self.dim_max:
            self.memoria.pop(0)
        self.memoria.append(experiencia)

    def amostrar(self, max_amostras: int):
        num_amostras = min(max_amostras, len(self.memoria))
        return random.sample(self.memoria, num_amostras)
