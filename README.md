<p align="center">
  <img width="200" height="84" src="https://github.com/OctaCoreWasTaken/qc-sim/blob/octa/CopProb_fix/qc-sim_logo.png">
</p>

# Instalation
To install the files of this project you can use `git clone https://github.com/OctaCoreWasTaken/qc-sim.git` in the terminal to clone
the repository. Having `git` installed is a requirement.

Once you have cloned the repository you may now execute the command `pip install -r requirements.txt` inside the 
newly created `qc-sim` folder. This will install all the requirements (libaries and packages) used by qc-sim automatically.

# Usage

To start, you import the module `qc_sim.py`. The `QUBITS` constant is a list of all the qubits in the computer. Each qubit has a set of logic gates:
  - `Sigma` - Puts the qubit in a superposition with the probability `P` in relation to the high energy state. Multiple `Sigma` gates followed by one another have their probabilities multiplied.
  - `Gamma` - Same as `Sigma` but in relation to the low energy state.
  - `Omega` - Acts as a CNOT gate and can entangle two qubits. `Q2` is refering to the target qubit.
  - `Measure` - Measures the qubit and has an effect on the outcome of `CopenhagenProbabilities`.

Outside the qubits there is a function called `CopenhagenProbabilities` which computes the probabilities of measurement being in the high
energy state. Feel free to report any related bugs.

Example program: `example.py`
```python
from qc_sim import *

QUBITS[0].Sigma(0.5) # Putting the qubit in a superposition.
QUBITS[0].Omega(QUBITS[1]) # Entangling the two qubits via CNOT.
QUBITS[0].Sigma(0.5) # Putting the qubit in a superposition again.
QUBITS[0].Measure() # Measuring the qubit. Function also returns the collapsed value.

p = CopenhagenProbabilities()
print(p[0],p[1]) # Printing the copenhagen probabilities of the two qubits q0 and q1.
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
> Admin mode is only for development and so it is not recommended to use it.
> Configuring the system wrong might lead to the simulator not working.

> [!NOTE]
> The core algorithm may be wrong in certain situations. If you find any issues please open a ticket.
