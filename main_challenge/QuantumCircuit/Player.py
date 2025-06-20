class Player:
    def __init__(self, name):
        self.name = name
        self.gates = {"H":1, "Z":1, "Y":1, "X":1, "CNOT":1, "SWAP":1}
    def get_gate(self):
        return dict(self.gates)