# qc-sim - Quality of life changes and better UI.
Quantum Simulator based on a brand new algorithm that aims to vastly improve speed and performance, allowing large quantum systems to be simulated.

# Instalation
This project is **not** on pypi so you cant just do `pip install qc-sim`. However that doesn't mean its not easy to install it!
To install the files of this project you can use `git clone https://github.com/OctaCoreWasTaken/qc-sim.git` in the terminal. 
All you need is ofcourse `git` installed.

# Usage

## Config
Configuring stuff is always annoying and so when i developed the `sim_config.py` application I made it as simple to use as possible!
Whenever you run the program in the terminal you will be greeted with a simple UI where you can see two buttons (On / Off) or you 
will see an input box. 
Inbetween the two buttons there will be some text with the name of the flag (ex: `FLAG_WARNING`) followed by it's state (On/Off).
Pressing the buttons will alter its state.
For the input box its the same. You can input any integer inside the box that is between 1 and 1000. 
Saving the changes is easy. You just have to press `S` and you will get sent to a screen where the program asks if you are sure.
Answering the prompt will revert you back to the home screen where based on your decision, your changes will be saved.

## Programming
Enough configuration! How about some programming?
To start, the `QUBIT` constant is a list of all the qubits in the computer. Each qubit has a set of logic gates:
> `Sigma` - Puts the qubit in a superposition with the probability `P` in relation to the high energy state. Multiple `Sigma` gates followed by one another have their probabilities multiplied.
> `Gamma` - Same as `Sigma` but in relation to the low energy state.
> `Omega` - Acts as a CNOT gate and can entangle two qubits. `Q2` is refering to the target qubit.
> `Measure` - Measures the qubit and has an effect on the outcome of `CopenhagenProbabilities`.

Outside the qubits there is a function called `CopenhagenProbabilities` which computes the probabilities of measurement being in the high
energy state. It is not finished so feel free to report bugs.

# What's new?
In this small branch update you can find some better UI. Such as a screen that prompts you "are you sure?" before saving in the config application.
Other than that there have been a few quality of life changes that allowed me to clean up some of my code.
