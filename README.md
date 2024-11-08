# qc-sim - Quality of life changes.
Quantum Simulator based on a brand new algorithm that aims to vastly improve speed and performance, allowing large quantum systems to be simulated.

# Instructions
`sim_config.py` is a terminal application that allows you to configure the quantum computer simulator.
Things such as: the warning flag, saving history flag and the number of qubits of the system.
The application has a simple and easy to use UI for better convenience.

Running the program in the terminal with the argument `--admin` will trigger the admin mode. This mode is specifically designed to change
some flags related to development. At the time of writing this, the only admin setting is the starting point flag which when enabled allows
the act of measurement to update the starting point for all qubits. This affects only CopenhagenProbabilities.
