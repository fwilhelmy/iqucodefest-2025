
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

class CircuitSimulator:

    def create_empty_circuit():
        qc = QuantumCircuit(2, 2)
        # Start with both qubits in |0>
        # Apply H to both as in original logic
        qc.h(0)
        qc.h(1)
        return qc
    
    def apply_circuit(qc):
    # Make a copy of the circuit
        try:
            qc_copy = qc.copy()
        except AttributeError:
            # For older Qiskit versions
            qc_copy = QuantumCircuit.from_qasm_str(qc.qasm())
        # Check if measurement already exists
        has_measure = any(instr[0].name == "measure" for instr in qc_copy.data)
        if not has_measure:
            qc_copy.measure(0, 0)
            qc_copy.measure(1, 1)
        sim = AerSimulator()
        result = sim.run(qc_copy).result()
        counts = result.get_counts()
        # Return the most probable result
        measured = max(counts, key=counts.get)
        return measured

    def reset_circuit():
        global qiskit_circuit, gate_history
        qiskit_circuit = create_empty_circuit()
        gate_history = [("H", 0), ("H", 1, "layer0")]