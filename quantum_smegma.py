from qiskit import QuantumCircuit, QuantumRegister, AncillaRegister, Aer, transpile, assemble
from qiskit.circuit.library import QFT
from math import gcd, log2
import matplotlib.pyplot as plt
from fractions import Fraction
from random import randint

# --- Modular Adder ---
def modular_adder(n, N):
    """Creates a quantum modular adder gate for fixed modulus N."""
    from qiskit.circuit import QuantumCircuit, QuantumRegister, AncillaRegister
    from qiskit.circuit.library import DraperQFTAdder

    acc = QuantumRegister(n, name='acc')  # The accumulator
    anc = AncillaRegister(n+2, name='anc')  # R.I.P ALL YOUR QUBITS
    qc = QuantumCircuit(acc, anc, name='ModAdd')

    adder = DraperQFTAdder(n)  # This is literally just making stuff more complex LOL
    qc.append(adder.to_gate(), acc)  # Accumulate errors and antidepressant bottles

    return qc.to_gate(label="ModAdd(N)")  # This is gonna haunt you

# --- Modular Multiplier: ---
def modular_multiplier(n, a, N):
    """Creates a gate that multiplies a by 2^x mod N. 
       You ever tried to escape math? It doesn’t let you out. Ever. Kinda hot amirite?"""
    x = QuantumRegister(n, name='x')
    acc = QuantumRegister(n, name='acc')
    anc = QuantumRegister(n+2, name='anc')
    qc = QuantumCircuit(x, acc, anc, name="ModMult")

    for i in range(n):
        a_shifted = (a * pow(2, i, N)) % N  # Shift by 2^i, but like, it's still you — miserable
        if a_shifted == 0:
            continue  # No escape. 
        mod_adder = modular_adder(n, N).control(1)  # Invoke the adder. Cry. Repeat.
        qc.append(mod_adder, [x[i]] + list(acc) + list(anc))

    return qc.to_gate(label="ModMult")  # We’re multiplying your existential dread by a factor of N and sending you a jury summons

# --- Modular Exponentiator ---
def modular_exponentiator(n, a, N):
    """This raises a to the power of 2^i mod N. It also calls you a bitchass nigga."""
    print("Bitchass nigga.")
    x = QuantumRegister(n, name='x')
    acc = QuantumRegister(n, name='acc')
    anc = AncillaRegister(n+2, name='anc')
    qc = QuantumCircuit(x, acc, anc, name="ModExp")

    qc.x(acc[0])  # Initialize acc = 1 — you had a good start, but it’s all downhill from here. Just like AttackLibrarian!

    for i in range(n):
        a_exp = pow(a, 2**i, N)  # 2^i, because we don’t take the easy route in Hell
        modmult = modular_multiplier(n, a_exp, N).control(1)
        qc.append(modmult, [x[i]] + list(acc) + list(anc))

    return qc.to_gate(label="ModExp")  # SHIT FUCK WHAT THE HELL DID I DO AND WHY DOESN'T THIS WORK ANY OTHER WAY

# --- Full Shor Circuit: Unholy fucking abomination ---
def build_shor_circuit(n, a, N):
    """I showed this to a mathematician I know and she started crying"""
    x = QuantumRegister(n, name='x')
    acc = QuantumRegister(n, name='acc')
    anc = AncillaRegister(n+2, name='anc')
    qc = QuantumCircuit(x, acc, anc)

    qc.h(x)  # Hadamard. Don't ask questions.

    for i in range(n):
        a_exp = pow(a, 2**i, N)
        ctrl_exp = modular_exponentiator(n, a_exp, N).control(1)
        qc.append(ctrl_exp, [x[n - 1 - i]] + list(acc) + list(anc))

    qc.append(QFT(n, do_swaps=True).inverse().to_gate(label="†QFT"), x)  # The inverse QFT — can math have a prolapse? FIND OUT NEXT TIME ON DRAGONBALL Z!

    qc.measure_all()  # Schroedinger's dick measuring contest

    return qc  # Abandon all hope.

# --- Classical Post-Processing: ---
def continued_fraction_expansion(x, denom):
    """"""
    frac = Fraction(x, denom).limit_denominator()
    return frac.denominator  # Epi is a bitch womp womp

def find_factors(a, N, r):
    """Find the factors. Will you find them? Nah. Only math, clinical depression, and a gcd function. ¯\_(ツ)_/¯"""
    if r % 2 != 0:
        return None  # womp womp
    candidate = pow(a, r // 2, N)
    if candidate == 1 or candidate == N - 1:
        return None  # Just like my parents love for me (NOT FOUND) ;_;
    factor1 = gcd(candidate + 1, N)
    factor2 = gcd(candidate - 1, N)
    return factor1, factor2  # Here's some fuckin factors. You want a fuckin sticker too, Dicksneeze?

# --- Run Shor's Algorithm ---
def run_shor(N):
    """This loops through different `a` values until it finds a way to tear N apart."""
    for _ in range(69):  # We try 69 times because Nice.
        a = randint(2, N - 1)
        if gcd(a, N) != 1:
            print(f"a = {a} is not coprime to N. Skipping.")  # This is you, forever stuck in a loop of failed attempts. Your parents must be so proud.
            continue  # Coprime? Nah bitch. The math gods don’t like you. I probably don't like you either.

        print(f"Attempting to factor N = {N} with base a = {a}")

        n = int(log2(N)) + 1  # Quantum register size based on N. FML why did I start this project
        qc = build_shor_circuit(n, a, N)

        # Simulate the circuit
        sim = Aer.get_backend('aer_simulator')  # PREPARE YOUR ANUS >:D
        tqc = transpile(qc, sim)
        qobj = assemble(tqc)
        result = sim.run(qobj).result()
        counts = result.get_counts()

        print("QPE Output:", counts)  # Do you realize how hard it is to get dead body stink out of a rug? Baking soda works best. Your simulation could use it here tbh

        measured = max(counts, key=counts.get)
        s = int(measured, 2)
        r = continued_fraction_expansion(s, 2**n)
        print(f"Estimated period r = {r}")

        # Use period r to find factors
        factors = find_factors(a, N, r)
        if factors:
            print(f"Factors of N = {N} are: {factors}")
            return factors  # I cried writing this but that might be because I sat on my balls idfk
        else:
            print(f"Failed to factor with a = {a}. Trying a new 'a'.")  # The cycle never ends.

    print("Unable to factor N within 69 attempts. Try different N or increase attempts.")  # GAME OVER INSERT COIN TO CONTINUE

# --- EXECUTE ---
if __name__ == "__main__":
    N = 2048  # RSA size. Run this on an IBM Osprey and watch your bank account cry.
    factors = run_shor(N)  # May God have mercy on your soul.