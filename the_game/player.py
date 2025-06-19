from dataclasses import dataclass, field
from collections import Counter

@dataclass
class Player:
    name: str
    position: int = 0                      # Space ID
    gates: Counter = field(default_factory=Counter)

    # ---- getters / setters ----
    def get_gates(self):      return dict(self.gates)
    def add_gates(self, gate:str, n:int=1): self.gates[gate] += n
    def set_name(self, new):  self.name = new
    def get_name(self):       return self.name
    def get_position(self):   return self.position
    def set_turn_priority(self, order): self.order = order

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
