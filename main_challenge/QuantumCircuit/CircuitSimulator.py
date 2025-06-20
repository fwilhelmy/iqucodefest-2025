from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel, depolarizing_error

class CircuitSimulator:

    def create_empty_circuit():
        qc = QuantumCircuit(2, 2)
        # Start with both qubits in |0>
        # Apply H to both as in original logic
        qc.h(0)
        qc.h(1)
        return qc

    def build_circuit_with_decoh(gate_history, decoh_error_rate):
        qc = QuantumCircuit(2, 2)
        for g in gate_history:
            if g[0] == "H":
                qc.h(g[1])
            elif g[0] == "X":
                qc.x(g[1])
            elif g[0] == "Y":
                qc.y(g[1])
            elif g[0] == "Z":
                qc.z(g[1])
            elif g[0] == "CNOT":
                qc.cx(g[1], g[2])
            elif g[0] == "SWAP":
                qc.swap(g[1], g[2])
            # Skip "DECOH" gates as they are for display only
        # Add measurement at the end
        qc.measure(0, 0)
        qc.measure(1, 1)
        return qc

    def apply_decoherence_noise(qc, percent):
        noise_model = NoiseModel()
        error_rate = percent / 100
        if error_rate > 0:
            # Apply depolarizing error to single-qubit gates
            single_qubit_error = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(single_qubit_error, ['h', 'x', 'y', 'z'])
            
            # Apply depolarizing error to two-qubit gates
            two_qubit_error = depolarizing_error(error_rate * 2, 2)
            noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx', 'swap'])
            
            # Apply depolarizing error to measurements
            measure_error = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(measure_error, ['measure'])
            
            return noise_model
        return None

    def apply_circuit(qc, noise_model=None, gate_history=None):
        if gate_history is not None:
            # Compute decoherence error rate: 10% per DECOH gate (max 100%)
            decoh_count = sum(1 for g in gate_history if g[0] == "DECOH")
            decoh_error_rate = min(1.0, decoh_count * 0.10)
            qc_copy = CircuitSimulator.build_circuit_with_decoh(gate_history, decoh_error_rate)
        else:
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
        result = sim.run(qc_copy, noise_model=noise_model, shots=1).result()
        counts = result.get_counts()
        # Return the most probable result
        measured = max(counts, key=counts.get)
        return measured
    
    def apply_decoherence_noise(qc, percent):
        noise_model = NoiseModel()
        error_rate = percent / 100
        if error_rate > 0:
            # Apply depolarizing error to single-qubit gates
            single_qubit_error = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(single_qubit_error, ['h', 'x', 'y', 'z'])
            
            # Apply depolarizing error to two-qubit gates
            two_qubit_error = depolarizing_error(error_rate * 2, 2)  # Scale error for 2-qubit gates
            noise_model.add_all_qubit_quantum_error(two_qubit_error, ['cx', 'swap'])
            
            # Apply depolarizing error to measurements
            measure_error = depolarizing_error(error_rate, 1)
            noise_model.add_all_qubit_quantum_error(measure_error, ['measure'])
            
            return noise_model
        return None
    
    def get_decoherence_percent():
    # Decoherence is now 10% per DECOH gate (max 100)
        decoh_gates = [g for g in gate_history if g[0] == "DECOH"]
        percent = min(100, len(decoh_gates) * 10)
        return percent

    def reset_circuit():
        global qiskit_circuit, gate_history
        qiskit_circuit = create_empty_circuit()
        gate_history = [("H", 0), ("H", 1, "layer0")]