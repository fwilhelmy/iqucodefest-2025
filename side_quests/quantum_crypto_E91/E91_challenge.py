"""
# E91 Quantum Key Distribution Protocol (Artur Ekert, 1991)

- Original paper: https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.67.661
- Algolab game: https://www.quantumcrypto.app/e91
- Wikipedia: https://en.wikipedia.org/wiki/Quantum_key_distribution#E91_protocol:_Artur_Ekert_.281991.29


## Objective
Alice and Bob establish a shared secret key using quantum entanglement. Security is based on the violation of Bell’s inequality, which detects any eavesdropping.

## Protocol Steps

1. **Preparation: Entangled Pair Generation**
   - A source generates many pairs of entangled qubits in a known Bell state.
   - Typically, the singlet state |Ψ-⟩ = (|01⟩ - |10⟩)/√2 is used.

2. **Distribution**
   - For each pair, one qubit is sent to Alice, the other to Bob.

3. **Random Basis Selection**
   - Alice randomly chooses a measurement basis for each qubit from: 0° (Z), 45°, or 90° (X).
   - Bob randomly chooses from: 45°, 90° (X), or 135°.
   - These choices are independent and random for each pair.

4. **Measurement**
   - Alice and Bob measure their qubits in their chosen bases.
   - For each pair, they record:
     - The chosen basis
     - The measurement results (0 or 1)

5. **Public Announcement of Bases**
   - After all measurements, Alice and Bob publicly share which basis they used for each qubit (but **not** the measurement results).

6. **Sifting: Data Partitioning**
   - For each pair:
     - If Alice and Bob used the **same basis** (both 45° or both 90°), keep the result for **key generation**.
     - If they used **specific pairs of different bases** (see below), keep the result for the **Bell (CHSH) test**.
     - **All other combinations are discarded** (e.g., (0°, 45°), (90°, 135°),).

   - **Key Generation Bases:** (45°, 45°) and (90°, 90°)
   - **CHSH Bell Test Bases:** (0°, 90°), (0°, 135°), (45°, 90°), (45°, 135°)
   - **Discarded Combinations:** All other basis pairs, such as (0°, 45°), (90°, 45°), (90°, 135°).

7. **Key Extraction**
   - For the key generation pairs, Alice and Bob use their measurement results to form their raw keys.
   - For the singlet state, results are anti-correlated: Bob flips his bits to match Alice’s.

8. **Bell Inequality (CHSH) Test**
   - Using the CHSH basis pairs, Alice and Bob compute the CHSH value (see separate file).
   - If |S| > 2, quantum entanglement is confirmed and the key is secure.
   - If |S| ≤ 2, eavesdropping or noise is detected and the key is discarded.

## Important Notes on Bell States

1. **Standard Implementation**: The original E91 protocol typically uses the singlet state (|Ψ-⟩). This state gives perfect anti-correlations when measured in the same basis.

2. **In Practice**: Any Bell state can be used for E91, as long as:
   - Alice and Bob know which Bell state they share
   - They adjust their measurement interpretations accordingly
   - They can verify entanglement via a Bell inequality test

3. **Realistic Simulation**: In practice, use a single type of Bell state for all pairs (usually |Φ+⟩ or |Ψ-⟩), and generate many copies of that same state.


## Example scenarios:  

alice_bases = ['0', '45', '90']
bob_bases = ['45', '90', '135']

chsh bell test bases alice = ['0', '45']
chsh bell test bases bob = ['90', '135']

- combinations for key generation (same bases): (45, 45), (90, 90)

- combinations for chsh bell test: (0, 90), (0, 135), (45, 90), (45, 135)

- other combinations are discarded: example (0, 45), (90,45), (90, 135)


## Coding Outline

1. Generate N Bell pairs.
2. Randomly assign bases to Alice and Bob for each pair.
3. Measure all pairs and record both the chosen bases and measurement results.
4. Publicly share bases, partition data into key generation, Bell test, and discarded sets.
5. Extract key bits and Bell test data.
6. Compute CHSH value; if secure, use the key.

# Note: The CHSH inequality calculation and test are implemented in a separate file.

## Additional Important Notes


- **Eavesdropping detection:**  
  The unique feature of E91 is that eavesdropping detection doesn't rely on comparing a subset of the key (as in BB84) but on the violation of Bell's inequality.  
  If an eavesdropper interferes with the entangled qubits, the quantum correlation will be disturbed, and Bell's inequality won't be violated as strongly as expected.

- **Statistical nature of CHSH:**  
  The CHSH value is a statistical measure that can be affected by the number of samples used.  
  With too few samples, random fluctuations may mask or mimic the effects of eavesdropping or noise.

"""

# E91 Quantum Key Distribution Protocol Implementation
import random
from qiskit import QuantumCircuit

import encryption_algorithms as enc # contains the encryption and decryption algorithms

random.seed(91) # do not change this seed, otherwise you will get a different key

import chsh_bell_inequality_challenge as bell # contains the CHSH Bell inequality functions

EVE_PERCENTAGE_COMPROMISED = 0.7 # Percentage of Bell pairs compromised by Eve


# E91 protocol basis definitions (change here if needed)
ALICE_BASES = ['0', '45', '90']
BOB_BASES = ['45', '90', '135']

# Bases used for CHSH Bell test (subsets of ALICE_BASES and BOB_BASES)
ALICE_CHSH_BASES = ['0', '90']
BOB_CHSH_BASES = ['45', '135']

# All allowed basis pairs for CHSH test (computed automatically)
CHSH_BASIS_PAIRS = [(a, b) for a in ALICE_CHSH_BASES for b in BOB_CHSH_BASES]
print('CHSH_BASIS_PAIRS : ', CHSH_BASIS_PAIRS)
# === E91 PROTOCOL FUNCTIONS ===

def generate_random_bases(length: int, options: list[str]) -> list[str]:
    """
    Generate a random list of measurement bases from the given options
    Args:
        length (int): The desired number of bases to generate (i.e., the length of the list).
        options (list[str]): A list of strings, where each string represents a
                             possible measurement basis (e.g., ['0', '45', '90'] for Alice,
                             or ['45', '90', '135'] for Bob).

    Returns:
        list[str]: A list of randomly selected bases, with the specified `length`.
    """
    # TODO: Student implementation goes here
    return [random.choice(options) for _ in range(length)] # gift from Algolab :p


def create_list_bell_pairs(num_pairs: int) -> list[QuantumCircuit]:
    """
    Creates a list of identical Bell pairs (the singlet state |Ψ-⟩).
    Each element in the list will be a QuantumCircuit object representing one Bell pair.

    Args:
        num_pairs (int): The number of Bell pair circuits to create.

    Returns:
        list[QuantumCircuit]: A list of `num_pairs` QuantumCircuit objects,
                              each prepared in the singlet Bell state |Ψ-⟩.
    """
    # TODO: Student implementation goes here
    # Hint: Use function from bell module
    pass

def measure_all_pairs(
    bell_pairs: list[QuantumCircuit],
    alice_bases: list[str],
    bob_bases: list[str]
) -> list[tuple[str, str]]:
    """
    Measures each Bell pair according to Alice's and Bob's chosen bases for that pair.

    Args:
        bell_pairs (list[QuantumCircuit]): A list of QuantumCircuit objects, where each
                                           circuit represents an entangled Bell pair.
        alice_bases (list[str]): A list of strings representing Alice's chosen measurement
                                 basis for each corresponding Bell pair in `bell_pairs`.
                                 The length of this list must be equal to `len(bell_pairs)`.
        bob_bases (list[str]): A list of strings representing Bob's chosen measurement
                               basis for each corresponding Bell pair in `bell_pairs`.
                               The length of this list must be equal to `len(bell_pairs)`.

    Returns:
        list[str]: A list str, each str is the measurement result string ('00', '01', etc.). Alice first bit, Bob second bit.
    """
    
    results: list[str] = []
    
    # TODO: Student implementation goes here
    # Hint: Use function from bell module

    return results


def extract_e91_key_and_bell_test_data(
    results: list[str],
    alice_bases: list[str],
    bob_bases: list[str],
    chsh_basis_pairs: list[tuple[str, str]] = CHSH_BASIS_PAIRS
) -> dict:
    """
    Sift the measurement results according to the E91 protocol rules:
      - Keep for key generation only if Alice and Bob used the same basis and that basis is 45° or 90° (i.e., (45,45) or (90,90)).
      - Keep for Bell (CHSH) test only if Alice and Bob used specific pairs of different bases: (0,90), (0,135), (45,90), (45,135).
      - Discard all other combinations.

    Args:
        results (list[str]): List of measurement results (e.g., '01', '10', ...), 
                             where the first bit is Alice's outcome and the second is Bob's.
        alice_bases (list[str]): List of Alice's chosen bases for each pair.
        bob_bases (list[str]): List of Bob's chosen bases for each pair.

    Returns:
        dict: {
            'key_results': list[str],         # Results for key generation (bases (45,45) or (90,90))
            
            'chsh_results': list[str],        # Results for CHSH Bell test
            'chsh_alice_bases': list[str],    # Alice's bases for CHSH test
            'chsh_bob_bases': list[str],      # Bob's bases for CHSH test
        }
    """
    
    key_results:list[str] = []

    chsh_results:list[str] = []
    chsh_alice_bases:list[str] = []
    chsh_bob_bases:list[str] = []

    # TODO: Student implementation goes here

    return {
        'key_results': key_results,
        'chsh_results': chsh_results,
        'chsh_alice_bases': chsh_alice_bases,
        'chsh_bob_bases': chsh_bob_bases,
    }
# ----------------------------------------

def check_for_eavesdropping(
    chsh_results: list[str],
    chsh_alice_bases: list[str],
    chsh_bob_bases: list[str]
) -> dict:
    """
    Check for eavesdropping using the Bell (CHSH) inequality test.

    Args:
        chsh_results (list[str]): Measurement results for CHSH test pairs (e.g., '01', '10', ...).
        chsh_alice_bases (list[str]): Alice's bases for CHSH test pairs.
        chsh_bob_bases (list[str]): Bob's bases for CHSH test pairs.

    Returns:
        dict: {
            'chsh_value': float,   # The calculated CHSH S-parameter
            'is_secure': bool      # True if Bell inequality is violated (|S| > 2), False otherwise
        }
    """
    # TODO: Student implementation goes here
    # Hint: Use function from bell module

    bell_chsh_value = None # change this    
    is_secure = None # change this

    return {
        'chsh_value': bell_chsh_value,
        'is_secure': is_secure
    }


def run_e91_protocol(
    num_pairs: int = 2000,
    eavesdropping: bool = False
) -> str | None:
    """
    Runs the complete E91 quantum key distribution protocol and returns the generated key if secure.

    Args:
        num_pairs (int): Number of entangled Bell pairs to generate and distribute. Default is 2000.
        eavesdropping (bool): If True, simulates eavesdropping on a percentage of Bell pairs.

    Returns:
        str | None: The generated shared secret key as a string of '0's and '1's if the
                    protocol is successful and secure. Returns None if the security check
                    fails or if no key bits are generated.

    Steps:
        1. Generate Bell pairs.
        2. Optionally simulate eavesdropping by compromising a percentage of pairs.
        3. Randomly assign measurement bases to Alice and Bob.
        4. Measure all pairs and record results.
        5. Sift results into key generation and CHSH Bell test data.
        6. Perform the CHSH test to check for eavesdropping.
        7. If secure, extract and return the shared key.
    """
    # TODO: Student implementation goes here

    print(f"Generate Bell pairs...")

    # Create a list of identical Bell pairs
    bell_pairs = create_list_bell_pairs(num_pairs)

    print(f"Number of Bell pairs: len(bell_pairs) : {len(bell_pairs)}")

    # Simulate eavesdropping if requested
    if eavesdropping:
        print(f"Simulate Eavesdropping: ")
        
        # nb of pairs compromised
        compromised_count = None # change this
        
        
        bell_pairs = None # change this

        print(f"Compromised pairs: {compromised_count} out of {num_pairs}")        
        print(f"Number of Bell pairs after eavesdropping: len(bell_pairs) : {len(bell_pairs)}")
    
    # Generate random bases for Alice and Bob : Set available bases using angle notation consistently
    alice_bases = generate_random_bases(num_pairs, ALICE_BASES)
    bob_bases = generate_random_bases(num_pairs, BOB_BASES)

    # TODO ... 
    
    return None # change this, return the key if secure, otherwise None


def decrypt_and_print_messages(key: str, filename: str = "encrypted_messages.txt"):
    """
    Read encrypted messages from a file, decrypt them using XOR with the given key, and print.

    Args:
        key (str): The key to use for XOR decryption.
        filename (str): The file to read encrypted messages from.
    """
    print("\nDecrypting all messages from", filename)
    
    # TODO: Student implementation goes here
    # Hint: Use enc.decrypt_xor_repeating_key from encryption_algorithms.py
    


def main():
    # Run the E91 protocol
    key = run_e91_protocol(num_pairs=2000, eavesdropping=True)
    
    if key:
        # Example usage: encrypt a message with the key
        message = '"What I cannot create, I do not understand." Richard Feynman.'
        print("\nOriginal message:", message)
        
        print("\nXOR encryption:")
        encrypted = enc.encrypt_xor_repeating_key(message, key)
        print("Encrypted:", encrypted)
        decrypted = enc.decrypt_xor_repeating_key(encrypted, key)
        print("Decrypted:", decrypted)
        
        print("\nCaesar cipher encryption:")
        encrypted = enc.encrypt_caesar_cipher(message, key)
        print("Encrypted:", encrypted)
        decrypted = enc.decrypt_caesar_cipher(encrypted, key)
        print("Decrypted:", decrypted)

        # For your challenge: must generate the correct key using the E91 protocol to decrypt the messages. Without the key, decryption is not feasible.
        print("\nDecrypting messages from file...")
        # TODO: change the path to the encrypted file as needed
        path_to_encrypted_file = R"encrypted_messages.txt"
        decrypt_and_print_messages(key, filename=path_to_encrypted_file)
        
    else:
        print("\nKey generation failed. Encryption cannot proceed.")



if __name__ == "__main__":
    main()