from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

_simulator = AerSimulator()

def controlled_displacement(qc):
        qc.mcx([0,1,2], 3, ctrl_state=None, mode='noancilla')
        qc.mcx([0,1], 2, ctrl_state=None, mode='noancilla')
        qc.mcx([0,], 1, ctrl_state=None, mode='noancilla')
        return qc

def quantum_walk_roll(step=6):
    """Return a dice roll using a quantum walk.
    """
    get_out = 0
    while get_out <= 1000:
        qc = QuantumCircuit(4, 3)
        qc.x(0)
        qc.h(0)
        random_walk_nb_steps = step
        for i in range(random_walk_nb_steps):
            qc = controlled_displacement(qc)
            qc.h(0)
        qc.measure([1, 2, 3], [0, 1, 2])
        qc.draw(output='mpl', filename='quantum_walk_roll.png')
        result = _simulator.run(qc, shots=1000).result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]
        value = int(outcome, 2)


        get_out += 1
        if value < 6: # s'assure qu'on reste entre 0 et 6
            return value + 1

