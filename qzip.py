# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
from qiskit import *
import numpy as np
import math
import random


# %%
# Define N to be factored:
N = 111

# Find L minimum no of bits to express N
L = int(math.ceil(math.log2(N)))

# Fine t to find the order of x
t = 7 #2 * L + 1

print("N =", N, " L =", L, " t =", t, " Total Number of Qubits =", L + t)


# %%
# Pick x at random between 1, N-1:
x = 11#random.randint(1, N)

print("x =", x)


# %%
# See if x has a GCD with N:
f1 = math.gcd(x, N)

# If there is a GCD then return the factor(f1):
print("Factor =", f1)


# %%
# If the factor is trivial i.e. 1, then there is no GCD
# between the 2 numbers; they are co-prime 
# -> construct Unitary of x^j mod N
iterations = 6#2**(int(L/2))

for i in range(1, iterations + 1):
    m = (x ** i) % N
    print(x,"^", i, " mod", N, " = ", m, " mod ", N)


# %%
# try with a imcomplete matirx U
U_data = np.zeros((2**L, 2**L))
print("DimU = ", U_data.shape)

# Fill the U with the mod values:
for i in range(1, iterations + 1):
    if i == 1 :
        prev_m = (x ** i) % N
    else:
        curr_m = (x ** i) % N
        
        U_data[prev_m][curr_m] = 1
        U_data[curr_m][prev_m] = 1
        prev_m = curr_m

for i in range(len(U_data)):
    if 1 not in U_data[i]:
        U_data[i][i] = 1

print(U_data)


# %%
# Create a unitary and convert it to a quantum gate
q, r = np.linalg.qr(U_data)

U_q = qiskit.extensions.UnitaryGate(q, label="U mod 111").control()


# %%
# Generate the quantum circuit for Shor's Algorithm:
shor = QuantumCircuit(t + L, t)

shor.h(range(t))
shor.x(t)

k = 0
for index in range(t):
    for i in range(2**k):
        shor.append(U_q, [index] + [i for i in range(t,t+L)])
    k += 1
    
shor.append(qiskit.circuit.library.QFT(t, inverse=True), range(t))
shor.measure(range(t), range(t))


# %%
# shor.draw('mpl')


# %%
from qiskit.visualization import plot_histogram

qasm_sim = Aer.get_backend('aer_simulator')
qasm_sim.set_options(device="GPU")
shots = 1024
results = execute(shor, backend=qasm_sim, shots=shots).result()
counts = results.get_counts(shor)
plot_histogram(counts, figsize=(30 , 10))


# %%
import pandas as pd
rows, measured_phases = [], []
for output in counts:
    if counts[output]/shots >= 0.1:
        decimal = int(output, 2)  # Convert (base 2) string to decimal
        phase = decimal/(2**t)  # Find corresponding eigenvalue
        measured_phases.append(phase)
        # Add these values to the rows in our table:
        rows.append([f"{output}(bin) = {decimal:>3}(dec)", 
                     f"{decimal}/{2**t} = {phase:.2f}"])
# Print the rows in a table
headers=["Register Output", "Phase"]
df = pd.DataFrame(rows, columns=headers)
print(df)


# %%
from fractions import Fraction
rows = []
for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(21)
    rows.append([phase, f"{frac.numerator}/{frac.denominator}", frac.denominator])
# Print as a table
headers=["Phase", "Fraction", "Guess for r"]
df = pd.DataFrame(rows, columns=headers)
print(df)


# %%

r = []
answer1 = []
answer2 = []

for phase in measured_phases:
    frac = Fraction(phase).limit_denominator(21)
    r.append(frac.denominator)
    if frac.denominator % 2 == 0:
        answer1.append(math.gcd(x ** int(r/2) - 1, N))
        answer2.append(math.gcd(x ** int(r/2) + 1, N))

print(answer1, answer2)


