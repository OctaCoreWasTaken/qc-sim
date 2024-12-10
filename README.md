<p align="center">
  <img width="300" height="125" src="https://github.com/OctaCoreWasTaken/qc-sim/blob/main/qc-sim_logo.png">
</p>

# Instalation
To install the files of this project you can use `git clone https://github.com/OctaCoreWasTaken/qc-sim.git` in the terminal to clone
the repository. Having `git` installed is a requirement.

Once you have cloned the repository you may now execute the command `pip install -r requirements.txt` inside the 
newly created `qc-sim` folder. This will install all the requirements (libaries and packages) used by qc-sim automatically.

# Usage

## Legacy version

To start, you import the module `qc_sim.py` and make sure the `FLAG_QC_LEGACY_MODE-dev` setting is turned on in the config. For more information check the **Config** section. The `QUBITS` constant is a list of all the qubits in the computer. Each qubit has a set of logic gates:
  - `Sigma` - Puts the qubit in a superposition with the probability `P` in relation to the high energy state. Multiple `Sigma` gates followed by one another have their probabilities multiplied.
  - `Gamma` - Same as `Sigma` but in relation to the low energy state.
  - `Omega` - Acts as a CNOT gate and can entangle two qubits. `Q2` is refering to the target qubit.
  - `Measure` - Measures the qubit

Outside the qubits there is a class called `MeasuringProbabilities` which contains a function named `Legacy` which computes the probabilities of measurement being in the high
energy state. Feel free to report any related bugs.

Example program: `example_legacy.py`
```python
from qc_sim import *

QUBITS[0].Sigma(0.5) # Putting the qubit in a superposition.
QUBITS[0].Omega(QUBITS[1]) # Entangling the two qubits via CNOT.
QUBITS[0].Sigma(0.5) # Putting the qubit in a superposition again.
QUBITS[0].Measure() # Measuring the qubit. Function also returns the collapsed value.

p = MeasuringProbabilities.Legacy(auto_display = True, qubit_nr_focus = 2) # Computing the Copenhagen probabilities and displaying them on a bar graph.
# qubit_nr_focus is the value which indicates which qubit probabilities are displayed. In this case, the 1st 2.
```
Example printout of: `example_legacy.py`:
```
                          _            
  __ _   ___         ___ (_) _ __ ___  
 / _` | / __| _____ / __|| || '_ ` _ \ 
| (_| || (__ |_____|\__ \| || | | | | |
 \__, | \___|       |___/|_||_| |_| |_|
    |_|                                
             = vX.X.Xx =-
---------------------------------------

WARNING: Printing of any particle counts as measurement and will collapse any superpostion!

─────── Copenhagen Probabilities - Legacy ────────
|00> ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 100.00
|01> ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 58.00
```

## Copenhagen-Style version

To start, you import the module `qc-sim.py`. This version of qc-sim allows you to simulate the classical quantum computer. The `QUBITS` constant contains a list of all the qubits in the computer. Each qubit contains a set of logic gates:
  - `X` (Pauli-X)
  - `Y` (Pauli-Y)
  - `Z` (Pauli-Z)
  - `H` (Hademard)
  - `P` (Phase)
  - `T` (π/8)
  - `CNOT` (Controlled Not)

There also is a class called `MeasuringProbabilities` which contains a function called `CopenhagenStyle` which computes the collapsing probability of 1 or more qubits in relation with eachother. In turn reconstructing the entagnlement relationship between 2 or more qubits.

Example program: `example_cphstyle.py`:
```python
from qc_sim import *

# Quantum circuit using the classical gates
QUBITS[0].H()
QUBITS[0].T()
QUBITS[0].H()
QUBITS[0].CNOT(QUBITS[1])
QUBITS[1].H()
QUBITS[1].T()
QUBITS[1].H()

# reconstructing the entanglement relationship between q0 and q1
MeasuringProbabilities.CopenhagenStyle(auto_display=True,focus_on_qubits_idx=[0,1])
```

Example printout of `example_cphstyle.py`:
```
                          _            
  __ _   ___         ___ (_) _ __ ___  
 / _` | / __| _____ / __|| || '_ ` _ \ 
| (_| || (__ |_____|\__ \| || | | | | |
 \__, | \___|       |___/|_||_| |_| |_|
    |_|                                
            -= vX.X.Xx =-
---------------------------------------

WARNING: Printing of any qubit... class counts as measurement and will collapse any superpostion!

─────── Copenhagen Probabilities - Current ───────
|00> ▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇▇ 72.59
|01> ▇▇▇▇▇▇▇ 12.56
|10> ▇ 2.17
|11> ▇▇▇▇▇▇▇ 12.68
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
