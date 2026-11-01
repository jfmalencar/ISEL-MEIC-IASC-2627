class Estado:
    def __init__(self, id_estado):
        self.id_estado = id_estado

    def __str__(self):
        return f"Estado({self.id_estado})"

    def __repr__(self):
        return f"Estado({self.id_estado})"

    def __hash__(self):
        return hash(self.id_estado)

    def __eq__(self, other):
        return isinstance(other, Estado) and self.id_estado == other.id_estado
