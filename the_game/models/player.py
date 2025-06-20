class Player:

    # ---- getters / setters ----
    def get_gates(self):      return self.gates
    def add_gates(self, gate:str, n:int=1): self.gates[gate] += n
    def set_gates(self, new_gates:dict):
        self.gates = new_gates
    def set_name(self, new):  self.name = new
    def get_name(self):       return self.name
    def get_position(self):   return self.position
    def set_turn_priority(self, order): self.order = order
    def set_sprite(self, surf): self.sprite = surf
    def __init__(self, slot):
        self.name: str = ""
        self.position: int = 0                      # Space ID
        # Players start with a basic set of Pauli gates so they can
        # immediately interact with the quantum board mechanics.
        self.gates: dict = {'H':0, 'X':1, 'Y':1, 'Z':1}  # starting gate counts
        self.slot = slot
        self.name = ""
        self.order = slot + 1
        self.sprite = None           # pygame Surface used when drawing
        self.color  = (0,0,0)        # fallback colour for pawn

    # ---- movement ----
    def move(self, steps:int, board:'Board'):
        """
        Move 'steps' spaces along the board graph.
        If a branch is encountered, let the board
        decide which way to go (could be AI, user input, or quantum).
        """
        current = self.position
        for _ in range(steps):
            next_options = board.spaces[current].next_spaces
            if not next_options:           # dead end
                break
            current = board.choose_branch(current, next_options, self)
        self.position = current
