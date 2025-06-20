import random
import networkx as nx
class Board:
    def __init__(self, spaces):
        self.spaces = {space.id: space for space in spaces}
        self.graph = nx.DiGraph()
        for space in spaces:
            for next_space in space.next_spaces:
                self.graph.add_edge(space.id, next_space)

    def get_next_spaces(self, space_id):
        """
        Get the next spaces from a given space ID.
        """
        return self.spaces[space_id].next_spaces if space_id in self.spaces else []

    def choose_branch(self, current, next_options, player):
        """
        Choose a branch based on the player's gates or randomly.
        """
        if not next_options:
            return current  # No options to choose from
        if player.gates:
            # Prefer a gate if available
            gate_choices = [opt for opt in next_options if opt in player.gates]
            if gate_choices:
                return random.choice(gate_choices)
        return random.choice(next_options)

    def draw_ascii(self):
        """
        Draw the board as an ASCII representation.
        """
        return "\n".join(str(space) for space in self.spaces.values())
