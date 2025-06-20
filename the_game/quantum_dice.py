from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

_simulator = AerSimulator()

def quantum_walk_roll():
    """Return a dice roll using a simple quantum walk.

    The circuit creates a uniform superposition over 3 qubits and measures it.
    Results 0-5 are mapped to dice values 1-6. Values 6 or 7 are retried.
    """
    while True:
        qc = QuantumCircuit(3, 3)
        qc.h([0, 1, 2])
        qc.measure([0, 1, 2], [0, 1, 2])
        result = _simulator.run(qc, shots=1).result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]
        value = int(outcome, 2)
        if value < 6:
            return value + 1

