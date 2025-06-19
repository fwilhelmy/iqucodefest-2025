# This part of code is by : Maxime Dion 
# Modified by ibra
import os

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle
from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

def plot_statevector(circuit):
    statevector = Statevector(circuit)
    state_indices = np.arange(len(statevector))
    n_qubits = int(np.log2(len(state_indices)))
    color_map = plt.get_cmap("jet")
    fig, ax_histo = plt.subplots(1, 1, figsize=(8, 4))
    ax_histo.bar(
        state_indices, np.abs(statevector), color=color_map(np.remainder(np.angle(statevector) / (2 * np.pi), 1))
    )
    ax_histo.set_xlabel("State", size="large")
    ax_histo.set_xticks(state_indices)
    ax_histo.set_xticklabels([f"{i:0{n_qubits}b}" for i in state_indices], size="large", rotation=60)
    ax_histo.set_ylabel("Amplitude", size="large")
    ax_histo.set_ylim(0, 1)

    fig.tight_layout()

    ax_phase = ax_histo.inset_axes((0.75, -0.18, 0.7, 0.7))  # Could be better

    # Inspired by qiskit qsphere code
    n = 64
    theta = np.ones(n)
    colors = color_map(np.remainder(np.arange(n) / n, 1))

    ax_phase.add_artist(
        Rectangle((-0.6, -0.6), width=1.2, height=1.2, facecolor="none", edgecolor="black", linewidth=0.7)
    )
    ax_phase.pie(theta, colors=colors, radius=0.4)
    ax_phase.add_artist(Circle((0, 0), 0.2, color="white", zorder=1))

    offset = 0.5

    labels = ["Phase", "$0$", "$\\pi/2$", "$\\pi$", "$3\\pi/2$"]

    ax_phase.text(0, 0, labels[0], horizontalalignment="center", verticalalignment="center", fontsize=14)
    ax_phase.text(offset, 0, labels[1], horizontalalignment="center", verticalalignment="center", fontsize=14)
    ax_phase.text(0, offset, labels[2], horizontalalignment="center", verticalalignment="center", fontsize=14)
    ax_phase.text(-offset, 0, labels[3], horizontalalignment="center", verticalalignment="center", fontsize=14)
    ax_phase.text(0, -offset, labels[4], horizontalalignment="center", verticalalignment="center", fontsize=14)

    plt.show()


def circuit_test():
    # Votre circuit ici
    circuit = QuantumCircuit(2)
    circuit.x(range(2))
    circuit.ry(np.pi/2,0)
    circuit.cx(0,1)
    circuit.s(1)

    return circuit

def main():
    qc = circuit_test()
    
    # Visualizer le circuit
    print(qc) #qc.draw('mpl', style="clifford")

    plot_statevector(qc)

if __name__ == '__main__':
    main()
