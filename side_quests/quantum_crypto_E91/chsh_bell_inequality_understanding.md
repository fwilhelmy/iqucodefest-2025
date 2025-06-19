# Understanding the CHSH Bell Inequality: Intuition, Steps, and Examples

*For students learning quantum information and the E91 protocol*

---

## Introduction

The **CHSH Bell inequality** is a fundamental test in quantum physics. It helps us decide if two particles (like qubits) are truly quantum entangled, or if their behavior can be explained by classical physics. This guide will walk you through the intuition, the steps, and the formulas, with concrete examples, so you can understand the meaning behind the chsh bell inequality.

---

## 1. The intuition: why Bell inequalities?

- **Classical World:** If two distant particles are measured, their results can be correlated, but only up to a certain limit. This is because, in classical physics, any "hidden" information they share must have been set before they were separated.
- **Quantum World:** If the particles are entangled, their measurement outcomes are correlated in a way that cannot be explained by classical physics. When you measure one particle, you immediately know what the outcome of measuring the other will be, even if they are far apart. This does **not** mean that measuring one physically changes the other at a distance; rather, their joint state was set up so that the outcomes are always correlated.

*For more, see:*
- [Stanford Encyclopedia of Philosophy: Quantum Entanglement and Information](https://plato.stanford.edu/entries/qt-entangle/)
- [John Preskill, Quantum Computation Lecture Notes, Section 4.2](http://theory.caltech.edu/~preskill/ph229/notes/chap4.pdf)
- [NIST: What is Quantum Entanglement?](https://www.nist.gov/news-events/news/2022/10/what-quantum-entanglement)

---

## 2. The CHSH Bell test: step by step

### **Step 1: Measurement Bases**

- **Alice** chooses between two measurement bases. In the standard CHSH test, these are often:
  `ALICE_BELL_BASES = ['0', '90']` (0° = Z-basis, 90° = X-basis)
- **Bob** also chooses between two measurement bases, often:
  `BOB_BELL_BASES = ['45', '135']` (45° and 135°)

> **Note:**  
> The CHSH test only requires that Alice and Bob each have two different measurement bases. The specific angles above are chosen because they maximize the quantum violation for the singlet state ($|Ψ-⟩ = (|01⟩ - |10⟩)/\sqrt{2}$), but in principle, you could use other angles. The important thing is to use all four combinations of Alice's and Bob's bases in the experiment.

#### Apply a measurement basis transformation to a qubit

Quantum measurements are typically performed in the Z-basis (measuring whether the qubit is |0⟩ or |1⟩). To measure in a different basis, we apply a unitary transformation (a set of quantum gates) that rotates the desired measurement basis to align with the Z-axis.

For the CHSH inequality, measurements are often performed in bases defined by angles in the X-Z plane of the Bloch sphere. We use Ry rotations for these transformations. An Ry(θ) gate rotates the qubit state around the Y-axis of the Bloch sphere by an angle θ.

To measure in a basis that is rotated by an angle 'angle_degrees' from the Z-axis towards the X-axis, we apply `Ry(-angle_radians)` to the qubit. This effectively rotates the qubit's state vector such that the desired measurement axis becomes the new Z-axis.

**Why Ry and not Rx or Rz?**
  - The angles (0°, 45°, 90°, 135°) are conventionally understood as angles in
      the X-Z plane of the Bloch sphere, starting from the +Z axis and moving
      towards the +X axis.
  - Ry rotations naturally map these axes onto each other while keeping states
      with real amplitudes (like superpositions of |0⟩ and |1⟩ without complex phases)
      as states with real amplitudes. This simplifies the visualization and understanding.
  - For example, to measure in the X-basis (eigenstates |+⟩ and |-⟩), which is at 90°from the Z-axis, we apply Ry(-π/2). This rotates |+⟩ to |0⟩ and |-⟩ to |1⟩.


### **Step 2: Running the Experiment**

For each entangled pair (singlet state):

1. **Randomly choose a basis for Alice and Bob.**  
   Example:  
   - Alice chooses `0` (Z-basis)
   - Bob chooses `45` (45° basis)

2. **Both measure their qubit in their chosen basis.**  
   - Each gets a result: `0` or `1`.

3. **Record:**  
   For each run, save the pair of bases used and the measurement result.  
   For example: `(0, 45): '10'`  
   - Here, Alice used base `0`, Bob used base `45`, and the result `'10'` means Alice measured `1` and Bob measured `0`.

   This format—pairing the chosen bases with the two-digit result string—makes it easy to group and analyze the outcomes later.
  
4. **Repeat** this process many times (e.g., 1000 pairs).  
   For each pair, Alice randomly chooses one of her two defined bases, and Bob randomly chooses one of his two defined bases.
   
---

### **Step 3: Organizing the Data**

After all measurements, **group the results** by the pair of bases used.  
There are 4 possible combinations:
- (Alice: `0`, Bob: `45`)
- (Alice: `0`, Bob: `135`)
- (Alice: `90`, Bob: `45`)
- (Alice: `90`, Bob: `135`)

For each combination, count how many times you got each possible outcome:
- `00`, `01`, `10`, `11`  
  (where the first digit is Alice’s result, the second is Bob’s)

**Example Table:**

| Alice Basis | Bob Basis | 00 | 01 | 10 | 11 |
|-------------|-----------|----|----|----|----|
| 0           | 45        | 120| 130| 130| 120|
| 0           | 135       | ...| ...| ...| ...|
| 90          | 45        | ...| ...| ...| ...|
| 90          | 135       | ...| ...| ...| ...|

---

### **Step 4: Calculating the Correlation for Each Basis Pair**

For each basis pair (e.g., Alice: `0`, Bob: `45`), calculate the **correlation**:

$$
E(a, b) = P(00) + P(11) - P(01) - P(10)
$$

Where:
- \(P(00)\), \(P(11)\), \(P(01)\), and \(P(10)\) are **probabilities** (or "fractions of times") that Alice and Bob get the respective outcomes when measuring with bases \(a\) and \(b\).
    - For example, \(P(00)\) is the number of times Alice gets 0 and Bob gets 0, divided by the total number of runs for that basis pair.
- In practice, you estimate these probabilities by running many experiments and counting outcomes. You can compute ( E(a, b) ) directly from your measurement counts as:

$$
E(a, b) = \frac{\text{count}(00) + \text{count}(11) - \text{count}(01) - \text{count}(10)}{\text{count}(00) + \text{count}(11) + \text{count}(01) + \text{count}(10)} 
$$

This formula is equivalent to the probability version above, but uses the actual number of times each outcome was observed.

**Why is it called \(E(a, b)\)?**  
- The "E" stands for **Expectation value** (or "expected value").  
- In quantum physics, the expectation value is the average value you expect to get if you repeat the experiment many times.  
- Here, \(E(a, b)\) is the expected value of the correlation between Alice's and Bob's results for measurement settings \(a\) and \(b\).

#### **Examples:**

- **Perfectly Correlated:**  
  Suppose Alice and Bob always get the same result (either `00` or `11`), each with 50% probability:
  - \(P(00) = 0.5\), \(P(11) = 0.5\), \(P(01) = 0\), \(P(10) = 0\)
  - \(E(a, b) = 0.5 + 0.5 - 0 - 0 = 1\)
  - **Interpretation:** Correlation = +1 (always agree)

- **Perfectly Anti-Correlated:**  
  Suppose they always get opposite results (`01` or `10`), each with 50% probability:
  - \(P(00) = 0\), \(P(11) = 0\), \(P(01) = 0.5\), \(P(10) = 0.5\)
  - \(E(a, b) = 0 + 0 - 0.5 - 0.5 = -1\)
  - **Interpretation:** Correlation = -1 (always disagree)

- **Completely Random:**  
  Suppose all outcomes are equally likely (25% each):
  - \(P(00) = 0.25\), \(P(11) = 0.25\), \(P(01) = 0.25\), \(P(10) = 0.25\)
  - \(E(a, b) = 0.25 + 0.25 - 0.25 - 0.25 = 0\)
  - **Interpretation:** Correlation = 0 (no correlation)

> **Reference:**
> - Nielsen & Chuang, *Quantum Computation and Quantum Information*, Eq. 2.77 
> [Google Books link (see page 92)](https://books.google.com/books?id=65FqEKQOfP8C&pg=PA92) 
> - [CHSH inequality, Wikipedia](https://en.wikipedia.org/wiki/CHSH_inequality)

---

### **Step 5: The CHSH Value (S)**

Now, use the **CHSH formula** to combine the correlations from all four measurement basis pairs:

\[
S = E(a_1, b_1) - E(a_1, b_2) + E(a_2, b_1) + E(a_2, b_2)
\]

Where:
- \(a_1 = 0\), \(a_2 = 90\) (Alice's two bases)
- \(b_1 = 45\), \(b_2 = 135\) (Bob's two bases)

So, in our standard example:

\[
S = E(0, 45) - E(0, 135) + E(90, 45) + E(90, 135)
\]

#### **Why this formula?**

- **Four combinations:** There are four possible pairs of measurement settings (two for Alice, two for Bob). The CHSH value combines all four to test the limits of classical versus quantum predictions.
- **The minus sign:** The placement of the minus sign is not arbitrary. It is essential to the mathematical structure of the CHSH inequality, which is derived from Bell's theorem. The specific arrangement of plus and minus signs ensures that, for any classical (local hidden variable) theory, the sum \( S \) cannot exceed 2 in absolute value. This structure allows the CHSH test to reveal the difference between classical and quantum correlations. If you used absolute values or changed the sign structure, the inequality would no longer distinguish between classical and quantum systems.
- **Different versions:** The sign convention can change depending on which Bell state you use, how you label outcomes, and the order of the bases. The important thing is: **for any classical system, |S| ≤ 2. For quantum entangled states, |S| can be up to 2√2 ≈ 2.828.**

> **References:**  
> - [Nielsen & Chuang, Section 2.2.5](https://books.google.com/books?id=65FqEKQOfP8C&pg=PA92)  
> - [Wikipedia: CHSH inequality](https://en.wikipedia.org/wiki/CHSH_inequality)
> - [Bell's theorem on Wikipedia](https://en.wikipedia.org/wiki/Bell%27s_theorem)

---

### **Step 6: Interpreting the Result**

- If |S| ≤ 2: The results could be explained by classical physics (no entanglement).
- If |S| > 2: The results show quantum entanglement (impossible classically).

| System    | Max \|S\| value   |
|-----------|------------------|
| Classical | 2                |
| Quantum   | 2√2 ≈ 2.828      |

---

## **Summary Table of Steps**

| Step | What Happens | Example |
|------|--------------|---------|
| 0 | Select initial pair of bases for Alice and Bob| `ALICE_BELL_BASES = ['0', '90']`, `BOB_BELL_BASES = ['45', '135']`|
| 1 | Generate the singlet state ||
| 2 | Alice & Bob randomly pick bases | Alice: 0, Bob: 45 |
| 3 | Both measure, get 0 or 1 | Alice: 1, Bob: 0 |
| 4 | Repeat many times | ... |
| 5 | Group results by basis pair | (0,45): 00=120, 01=130, ... |
| 6 | Compute E(a,b) for each pair | E(0,45) = -0.04 |
| 7 | Plug into CHSH formula | S = ... |
| 8 | Interpret S | If |S| > 2, quantum! |

---

## **Further Reading**

- [Stanford Encyclopedia of Philosophy: Quantum Entanglement and Information](https://plato.stanford.edu/entries/qt-entangle/)
- [John Preskill, Quantum Computation Lecture Notes, Section 4.2](http://theory.caltech.edu/~preskill/ph229/notes/chap4.pdf)
- [Nielsen & Chuang, Quantum Computation and Quantum Information](https://books.google.com/books?id=65FqEKQOfP8C&pg=PA92)
- [Wikipedia: CHSH inequality](https://en.wikipedia.org/wiki/CHSH_inequality)

---

*Now that you understand the intuition and the steps, you’re ready to dive into the code!*