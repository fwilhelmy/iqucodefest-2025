# iQuCodeFest 2025

Welcome to the official repository for iQuCodeFest 2025!

This repository contains all the files, notebooks, and resources for the quantum computing hackathon taking place on June 19th and 20th, 2025, at `Polytechnique Montréal`.

## Repository Structure

### 1. Tutorials
**`tutorials/`**
This folder is designed for beginners with little or no prior experience in quantum computing. It contains three challenges to help you get started:
- **`intro_qiskit`**: Introductory notebooks on quantum computing concepts using Qiskit. Includes explanations, example code, and exercises to reinforce your understanding.
- **`bloch_sphere_dojo`**: Learn about quantum gates and visualize their effects on the Bloch sphere.
- **`quantum_dojo`**: Understand quantum states (e.g., $|\psi⟩$) and the quantum circuits that generate them.

### 2. Side quests
**`side_quests/`**
This directory includes a set of intermediate-level challenges:
- **Teleportation & Superdense Coding**
- **Quantum Cryptography (E91)**
  - CHSH Bell Inequality
  - E91 Protocol
- **QAOA (Quantum Approximate Optimization Algorithm)**

### 3. Main Challenge
**`main_challenge/`**
This folder contains the main hackathon challenge:
- **`iQuCodeFest_Rule_Book.pdf`**: Detailed description of the Quantum Board Game Challenge.

#### Quantum Board Game Challenge Summary
Participants are invited to reimagine classic games by integrating quantum principles—such as superposition, entanglement, and quantum measurement—directly into the rules or gameplay. The goal is not to solve classical problems with quantum computers, but to create new, quantum-inspired versions of familiar games that showcase creativity and a deeper understanding of quantum concepts.

Please refer to the iQuCodeFest Rule Book for more details.

---

## Setup and Installation

To set up your environment:

1. **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd iQuCodeFest_2025
    ```
2. **(Recommended) Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. **Install required packages:**
    ```bash
    pip install -r requirements.txt
    ```

For detailed setup instructions and troubleshooting, refer to `python_project_setup_guide.md`.

---

You now have all the tools and resources needed to participate in the hackathon. Good luck and have fun exploring quantum computing!