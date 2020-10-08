"""Simple quantum computations simulation."""

import numpy as np


def I():
  """Identity operator."""
  return np.identity(2)

def X():
  """X-rotation, negation operator."""
  return np.identity(2)[..., ::-1]

def H():
  """Adamara operator, superposition."""
  return np.array([[1, 1], [1, -1]]) / np.sqrt(2)

def SWAP():
  """Swap 2 qubits"""
  m = np.identity(4)
  m[[1, 2]] = m[[2, 1]]
  return m

def CX():
  """Controlled negation."""
  m = np.identity(4)
  m[[3, 2]] = m[[2, 3]]
  return m


def apply(v, *gates):
  m = gates[0]
  gates = gates[1:]
  for gate in gates:
    m = np.kron(gate, m)
  return m.dot(v)

def observe(v):
  v2 = np.absolute(v) ** 2
  c = np.random.choice(v.size, 1, p=v2)
  return c[0]


# Usage example
# create 3 qubits in state 000, array size 2 ^ n
a = np.array([1, 0, 0, 0, 0, 0, 0, 0])

# transform the 2nd qubit into a superposition of 0 and 1
a = apply(a, I(), H(), I())

# entangle the 1st and 2nd qubit
a = apply(a, CX(), I())

# swap the 2nd and 3rd qubit
a = apply(a, I(), SWAP())

# observe the state
observe(a)
