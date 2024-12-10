import numpy as np
import copy
from dependencies.sim_dependencies import *
from dependencies.plot import *
from tqdm import tqdm

MEASUREMENT_MODE_EV = 0
MEASUREMENT_MODE_BIN = 1
FLAG_WARNING = False
FLAG_INITIALIZED = False
FLAG_RECORD_HISTORY = False
GLOBAL_HISTORY_TYPE = ""
GLOBAL_HISTORY = []
GLOBAL_STARTING_POINT = []
QUBIT_NUMBER = 0
FLAG_STARTING_POINT = True
FLAG_QC_SIM = False
FLAG_QC_LEGACY_MODE = False
FLAG_CONTINUE_ON_ERROR = False
# DONT FORGET TO UPDATE
VERSION = "snapshot v0.0.7g" # Merge 7, variation g
FLAG_RELEASE = False

json_file = read_json()
for item in json_file.items():
    if item[0] == "FLAG_WARNING":
        FLAG_WARNING = True if item[1] == "On" else False
    if item[0] == "FLAG_RECORD_HISTORY":
        FLAG_RECORD_HISTORY = True if item[1] == "On" else False
    if item[0] == "QUBIT_NUMBER":
        QUBIT_NUMBER = item[1]
    if item[0] == "FLAG_STARTING_POINT-dev":
        FLAG_STARTING_POINT = True if item[1] == "On" else False
    if item[0] == "FLAG_QC_SIM":
        FLAG_QC_SIM = True if item[1] == "On" else False
    if item[0] == "FLAG_QC_LEGACY_MODE-dev":
        FLAG_QC_LEGACY_MODE = True if item[1] == "On" else False
    if item[0] == "FLAG_CONTINUE_ON_ERROR":
        FLAG_CONTINUE_ON_ERROR == True if item[1] == "On" else False
    
if FLAG_QC_SIM:
    print(art.text2art("qc-sim") + " " * (round(16 - len(VERSION) / 2) + 1) + f"-= {VERSION} =-")
    print("-" * 39 + "\n")

#########################
###                   ###
### --- UNIVERSAL --- ###
###                   ###
#########################

def Error_msg(text):
    print(bcolors.FAIL + bcolors.BOLD + text + bcolors.ENDC)

def Warning_msg(text):
    print(bcolors.WARNING + bcolors.BOLD + text + bcolors.ENDC)

def ContinueOnErrorWarning():
    if FLAG_CONTINUE_ON_ERROR: Warning_msg("WARNING: CONTINUE ON ERROR is on! The application will resume execution!")
    else: exit()

class MeasuringProbabilities:
    def Legacy(mm: int = MEASUREMENT_MODE_BIN,iterations: int = 100,auto_display: bool = False, fancy_plot: bool = False, qubit_nr_focus: int = QUBIT_NUMBER):
        """Simple to use function to compute probabilities of relationships between qubits (entanglement)
           or the collapsing probability of a single qubit in a given circuit. And to display in a 
           convenient way its results.
           """
        global FLAG_RECORD_HISTORY
        if FLAG_RECORD_HISTORY:
            if GLOBAL_HISTORY_TYPE != "Legacy":
                Error_msg("ERROR: MeasuringProbabilities.Legacy: Wrong history type!")
                ContinueOnErrorWarning()
            FLAG_RECORD_HISTORY = False
            eVs = []
            for i,qubit in enumerate(QUBITS):
                eVs.append(qubit.energy_level)
                QUBITS[i].energy_level = copy.deepcopy(GLOBAL_STARTING_POINT[i].energy_level)
            low = np.array([0 for i in range(QUBIT_NUMBER)])
            high = np.array([0 for i in range(QUBIT_NUMBER)])
            for i in tqdm(range(iterations),leave=False):
                for action in GLOBAL_HISTORY:
                    if len(action) == 2:
                        QUBITS[action[1]].energy_level = copy.deepcopy(action[0])
                    elif len(action) == 3:
                        action[0](action[1],action[2])
                    else:
                        action[0](action[1],QUBITS[action[2]])
                for i, q in enumerate(QUBITS):
                    if q.energy_level == q.low_orbit_energy:
                        low[i] += 1
                        q.energy_level = copy.deepcopy(GLOBAL_STARTING_POINT[i].energy_level)
                    else:
                        high[i] += 1
                        q.energy_level = copy.deepcopy(GLOBAL_STARTING_POINT[i].energy_level)
            low = low / float(iterations)
            high = high / float(iterations)
            qubit_low_orbitals = [q2.low_orbit_energy for q2 in QUBITS]
            qubit_high_orbitals = [q3.high_orbit_energy for q3 in QUBITS]
            FLAG_RECORD_HISTORY = True
            if not auto_display:
                return np.add(np.multiply(low,qubit_low_orbitals),np.multiply(high,qubit_high_orbitals)) * 0.5 if mm == MEASUREMENT_MODE_EV else high
            category_names = [f"|{"0" * (len(str(bin(qubit_nr_focus))) - len(str(bin(x)))) + str(bin(x))[2:]}>" for x in range(qubit_nr_focus)]
            plot_values = high[:qubit_nr_focus] * 100
            # print(plot_values)
            if fancy_plot: barplot_fancy(category_names,plot_values,"Copenhagen Probabilities - Legacy"); return
            barplot(category_names,plot_values,"Copenhagen Probabilities - Legacy",width=50)
            print("")
            return
        Error_msg("ERROR: MeasuringProbabilities.Legacy: Cannot compute Copenhagen probabilities! Missing history! Consider enabling FLAG_RECORD_HISTORY!")
        ContinueOnErrorWarning()
    def CopenhagenStyle(iterations: int = 100, auto_display: bool = False, fancy_plot: bool = False, focus_on_qubits_idx: list = range(QUBIT_NUMBER)):
        """
            Simple to use function to compute the probabilities of a relationship between 2 or more qubits (entanglement)
            or to compute the collapsing probabilities of a qubit in a given circuit. And to display the results in a
            convenient matter.
        """
        global FLAG_RECORD_HISTORY
        if FLAG_RECORD_HISTORY:
            if GLOBAL_HISTORY_TYPE != "Copenhagen-style":
                Error_msg("ERROR: MeasuringProbabilities.CopenhagenStyle: Wrong history type!")
                ContinueOnErrorWarning()
            FLAG_RECORD_HISTORY = False
            starting_point = GLOBAL_STARTING_POINT
            fake_qubits = copy.deepcopy(starting_point)
            qubits_on_focus = focus_on_qubits_idx
            high = [0 for i in range(2**len(qubits_on_focus))]
            max_len = len(str(bin(2**len(qubits_on_focus) - 1))) - 2
            for iteration in tqdm(range(iterations),leave=False):
                for action in GLOBAL_HISTORY:
                    if len(action) == 2:
                        fake_qubits[action[1]].matrix = action[0](fake_qubits[action[1]].matrix)
                    if len(action) == 3:
                        fake_qubits[action[1]].__m__()
                        fake_qubits[action[2]].__m__()
                        fake_qubits[action[2]].matrix = action[0](fake_qubits[action[1]].matrix,fake_qubits[action[2]].matrix)
                for i in range(QUBIT_NUMBER):
                    fake_qubits[i].__m__()
                for case in range(2**len(qubits_on_focus)):
                    case_string = "0" * (max_len - len(str(bin(case))[2:])) + str(bin(case))[2:]
                    result_and = True
                    for j, qubit_idx in enumerate(qubits_on_focus):
                        result_and = result_and and (int(fake_qubits[qubit_idx].Probability()) == int(case_string[j]))
                    if result_and: high[case] += 1
                for i in range(QUBIT_NUMBER):
                    fake_qubits[i].matrix = copy.deepcopy(starting_point[i].matrix)
                
            high = np.array(high)
            high = high / iteration
            FLAG_RECORD_HISTORY = True
            if not auto_display:
                return high
            category_names = [f"|{"0" * (max_len - len(str(bin(i))) + 2) + str(bin(i))[2:]}>" for i in range(2**len(focus_on_qubits_idx))]
            plot_values = high * 100
            if not fancy_plot: barplot(category_names,plot_values,"Copenhagen Probabilities - Current",50); print(""); return
            barplot_fancy(category_names,plot_values,"Copenhagen Probabilities - CphStyle")
            return
        Error_msg("ERROR: MeasuringProbabilities.CopenhagenStyle: Cannot compute Copenhagen probabilities! Missing history! Consider enabling FLAG_RECORD_HISTORY!")
        ContinueOnErrorWarning()



##############################
###                        ###
### --- LEGACY VERSION --- ###
###                        ###
##############################

def __Po2__(self,Ee: float) -> float:
    """Sub-version of _Po2 used for CopenhagenProbabilities"""
    d = self.high_orbit_energy - self.low_orbit_energy
    return np.sin(((Ee - d/2) * np.pi) / 5) * 0.5 + 0.5

def __Sigma__(self,P: float) -> None:
    """Sub-version of Sigma used for CopenhagenProbabilities"""
    s = -1 if self.energy_level > self.low_orbit_energy else 1
    Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    po2 = __Po2__(self,Ee)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    self.energy_level = collapse

def __rSigma__(self,P:float) -> float:
    """Sub-version of _Sigma used for CopenhagenProbabilities"""
    s = -1 if self.energy_level > self.low_orbit_energy else 1
    return self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s

def __Gamma__(self,P: float) -> None:
    """Sub-version of Gamma used for CopenhagenProbabilities"""
    s = 1 if self.energy_level > self.low_orbit_energy else -1
    Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    po2 = __Po2__(self,Ee)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    self.energy_level = collapse

def __Omega__(self,P2) -> None:
    """Sub-version of Omega used for CopenhagenProbabilities"""
    Ee2 = ((self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)) * __rSigma__(P2,1)
    po2 = __Po2__(self,Ee2)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    P2.energy_level = collapse

class Qubit_Classic:
    """
       **Brief explanation of the Classic / Legacy algorithm**
        
        Simple algorithm for simulating a new type of a quantum computer meant to improve performance
        and efficiency exponentially with the number of qubits.
        
        The algorithm describes a qubit as being an atom where we send
        and amount of energy to it related to a given probability. This combined with some random
        energy (temperature whenever we count multiple atoms) gives us a probability of whether it
        will or not ionize. Giving us 2 stable states. On and off.

        Licensed under MPL-2.0 - OctaCore 2024
        """
    def __init__(self,index: int,mm: int = MEASUREMENT_MODE_EV) -> None:
        global FLAG_INITIALIZED
        self.index = index
        self.low_orbit_energy = -10 # eV
        self.energy_level = self.low_orbit_energy
        self.high_orbit_energy = -5 # eV      
        self.measurement_mode = mm

    def _Po2(self,Ee: float) -> float:
        """Computes the probability of any given energy state, especially inbetween. Unrealistic.
           Used for implmenting collapsing of the qubits."""
        d = self.high_orbit_energy - self.low_orbit_energy
        return np.sin(((Ee - d/2) * np.pi) / 5) * 0.5 + 0.5
    
    def _Sigma(self,P: float) -> float:
        """Low level version of Sigma. Returns the energy level before collapsing. Unrealistic. 
           Used for implementing Omega."""
        s = -1 if self.energy_level > self.low_orbit_energy else 1
        return self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    
    def Sigma(self,P: float) -> None:
        """Allows for easy superposition manipulation in relation to the 1 (down or in this case up) state. 
           !! Applying multiple of these gates in series multiplies their probabilities rather than adding 
           the energy being sent."""
        s = -1 if self.energy_level > self.low_orbit_energy else 1
        Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
        po2 = self._Po2(Ee)
        collapse = np.random.default_rng().choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
        self.energy_level = collapse
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Sigma__,self,P])

    def Omega(self,Q2) -> None:
        """Acts as the CNOT gate and entangles qubit states."""
        if type(Q2) == Qubit_Classic:
            Ee2 = ((self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)) * Q2._Sigma(1)
            po2 = self._Po2(Ee2)
            collapse = np.random.default_rng().choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
            Q2.energy_level = collapse
            if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Omega__,self,Q2.index,None])
            return
        Error_msg("ERROR: Qubit_Classic.Omega: Q2 is not a Qubit_Classic class!")
        ContinueOnErrorWarning()
            
    def Gamma(self,P: float) -> None:
        """Allows for easy superposition manipulation in relation to the 0 (up or in this case down) state. 
           !! Applying multiple of these gates in series multiplies their probabilities rather than adding 
           the energy being sent."""
        s = 1 if self.energy_level > self.low_orbit_energy else -1
        Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
        po2 = self._Po2(Ee)
        collapse = np.random.default_rng().choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
        self.energy_level = collapse
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Gamma__,self,P])

    def Measure(self) -> None:
        """Measures and collapses the value of the given qubit class."""
        global GLOBAL_HISTORY, GLOBAL_STARTING_POINT
        GLOBAL_HISTORY.append([self.energy_level,self.index])
        # if FLAG_RECORD_HISTORY: GLOBAL_HISTORY = [] 
        # if FLAG_STARTING_POINT: GLOBAL_STARTING_POINT = copy.deepcopy(QUBITS)
        return self.energy_level if self.measurement_mode == MEASUREMENT_MODE_EV else (self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy) 

    def __m__(self) -> None:
        """WARNING: DO NOT USE THIS FUNCTION. THIS IS DEVELOPMENT ONLY"""
        return (self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)

    def __str__(self) -> None:
        return bcolors.OKCYAN + str(self.Measure()) + bcolors.ENDC

################################
###                          ###
### --- COPENHAGEN-STYLE --- ###
###                          ###
################################


def prob(ket: np.ndarray) -> float:
    """Individual probability of the qubit"""
    return abs(ket[1])**2

def ket_0() -> np.ndarray:
    """Returns |0>"""
    return np.array([1,0])

def ket_1() -> np.ndarray:
    """Returns |1>"""
    return np.array([0,1])

# PAULI-X
def X(q: np.ndarray) -> np.ndarray:
    """Pauli-X gate"""
    return q @ np.array([[0,1],[1,0]])

# PAULI-Y
def Y(q: np.ndarray) -> np.ndarray:
    """Pauli-Y gate"""
    return q @ np.array([[0,-1j],[1j,0]])

# PAULI-Z
def Z(q: np.ndarray) -> np.ndarray:
    """Pauli-Z gate"""
    return q @ np.array([[1,0],[0,-1]])

# HADAMARD
def H(q: np.ndarray) -> np.ndarray:
    """Hademard gate"""
    return q @ (1/np.sqrt(2) * np.array([[1,1],[1,-1]]))

# PHASE
def S(q: np.ndarray) -> np.ndarray:
    """Phase gate"""
    return q @ np.array([[1,0],[0,1j]])

# π/8
def T(q: np.ndarray) -> np.ndarray:
    """π/8 gate"""
    return q @ np.array([[1,0],[0,np.exp(1j * np.pi / 4)]])

# CONTROLLED NOT
def CNOT(q0: np.ndarray,q1: np.ndarray) -> np.ndarray:
    """CNOT gate"""
    I = np.array([[1,0],[0,1]])
    X = np.array([[0,1],[1,0]])
    return q1 @ (prob(q0) * X + (1 - prob(q0)) * I)

# MEASURE
def M(q: np.ndarray) -> np.ndarray:
    """Measurement gate"""
    p = prob(q)
    if np.random.default_rng().choice([0,1],p=[1-p,p]) == 0:
        return ket_0()
    return ket_1()


class Qubit:
    """
       Simple and elegant solution for simulating classic quantum computers faster
       
       Licensed under MPL-2.0 - OctaCore 2024
       """
    def __init__(self, index: int):
        self.index = index
        self.matrix = ket_0() # |0>

    # PAULI-X
    def X(self) -> None:
        """Pauli-X gate"""
        self.matrix = X(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([X,self.index])

    # PAULI-Y
    def Y(self) -> None:
        """Pauli-Y gate"""
        self.matrix = Y(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([Y,self.index])

    # PAULI-Z
    def Z(self) -> None:
        """Pauli-Z gate"""
        self.matrix = Z(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([Z,self.index])

    # HADAMARD
    def H(self) -> None:
        """Hademard gate"""
        self.matrix = H(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([H,self.index])

    # PHASE
    def S(self) -> None:
        """Phase gate"""
        self.matrix = S(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([S,self.index])

    # π/8
    def T(self) -> None:
        """π/8 gate"""
        self.matrix = T(self.matrix)
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([T,self.index])

    # CONTROLLED NOT
    def CNOT(self,target) -> None:
        """CNOT gate"""
        if type(target) == Qubit:
            self.matrix = M(self.matrix)
            target.matrix = M(target.matrix)
            self.matrix = CNOT(self.matrix,target.matrix)
            if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([CNOT,self.index,target.index])
            return
        Error_msg("ERROR: Qubit.CNOT: target is not a Qubit class!")
        ContinueOnErrorWarning()

    # PROBABILITY
    def Probability(self) -> float:
        """WARNING: This function returns a collapsing probability
           which does **NOT** take entanglement into account!"""
        return prob(self.matrix)

    # MEASURE (internal)
    def __m__(self) -> None:
        """WARNING: This function is for development use only!"""
        self.matrix = copy.deepcopy(M(self.matrix))
    
    # MEASURE (external)
    def M(self) -> None:
        """Measurement gate"""
        self.__m__()
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([M,self.index])
        return self.matrix

    # MEASURE AND PRINT
    def __str__(self) -> None:
        self.M()
        return bcolors.OKCYAN + str(self.Probability()) + bcolors.ENDC

if not FLAG_INITIALIZED and FLAG_WARNING:
    Warning_msg("WARNING: Printing of any qubit... class counts as measurement and will collapse any superpostion!")
    if not FLAG_RELEASE: Warning_msg("WARNING: The current version of qc-sim is not a release! Any new feature might include bugs!")
    print("")
    FLAG_INITIALIZED = True

if FLAG_QC_LEGACY_MODE:
    QUBITS = [Qubit_Classic(x,MEASUREMENT_MODE_BIN) for x in range(QUBIT_NUMBER)]
    GLOBAL_HISTORY_TYPE = "Legacy"
else:
    QUBITS = [Qubit(x) for x in range(QUBIT_NUMBER)]
    GLOBAL_HISTORY_TYPE = "Copenhagen-style"
GLOBAL_STARTING_POINT = copy.deepcopy(QUBITS)