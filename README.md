# qc-sim - Quantum Computer Simulator
An algorithm designed to simulate quantum computers faster and more efficient.

> [!NOTE]
> The core algorithm may be wrong in certain situations. If you find any issues please open a ticket.

# Instalation
To install the files of this project you can use `git clone https://github.com/OctaCoreWasTaken/qc-sim.git` in the terminal to clone
the repository. Having `git` installed is a requirement.

# Usage

To start, you import the module `qc_sim.py`. The `QUBIT` constant is a list of all the qubits in the computer. Each qubit has a set of logic gates:
  - `Sigma` - Puts the qubit in a superposition with the probability `P` in relation to the high energy state. Multiple `Sigma` gates followed by one another have their probabilities multiplied.
  -`Gamma` - Same as `Sigma` but in relation to the low energy state.
  - `Omega` - Acts as a CNOT gate and can entangle two qubits. `Q2` is refering to the target qubit.
  - `Measure` - Measures the qubit and has an effect on the outcome of `CopenhagenProbabilities`.

Outside the qubits there is a function called `CopenhagenProbabilities` which computes the probabilities of measurement being in the high
energy state. Feel free to report any related bugs.

Example program: `example.py`
```python
from qc_sim import *

QUBITS[0].Sigma(0.5) # Putting the qubit in a superposition.
QUBITS[0].Omega(QUBITS[1]) # Entangling the two qubits via CNOT.
print(QUBITS[0],QUBITS[1]) # Measuring the two qubits and printing the result.
```

## Config
Using `sim_config.py` you can easily configure different flags and settings of the quantum computer simulation such as the number of
qubits.

> [!IMPORTANT]
> The flag `FLAG_RECORD_HISTORY` enables storing of all the gates in the circuit before the last measurement. 
> `CopenhagenProbabilities` uses this data, and so it must be enabled when using said function.

> [!TIP]
> If you are not using `CopenhagenProbabilities` disabling the `FLAG_RECORD_HISTORY` flag will allow the program to run faster and
> take up less space. More useful the more gates you use.

Running `sim_config.py` with the argument `--admin` will trigger admin mode enabling access to a few more settings.

> [!WARNING]
> Using the admin mode is only for development and it is not recommend to use it, because you could end up
> disabling or enabling some flags that will make the simulation run wrong.
