import json
import numpy as np

MEASUREMENT_MODE_EV = 0
MEASUREMENT_MODE_BIN = 1
FLAG_WARNING = False
FLAG_INITIALIZED = False
FLAG_RECORD_HISTORY = False
GLOBAL_HISTORY = []
QUBIT_NUMBER = 0

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def read_json():
    with open('qc_sim_DIP_settings.json','r') as openfile:
        json_file = json.load(openfile)
    return json_file

json_file = read_json()
for item in json_file.items():
    if item[0] == "FLAG_WARNING":
        FLAG_WARNING = True if item[1] == "On" else False
    if item[0] == "FLAG_RECORD_HISTORY":
        FLAG_RECORD_HISTORY = True if item[1] == "On" else False
    if item[0] == "QUBIT_NUMBER":
        QUBIT_NUMBER = item[1]

def __Po2__(self,Ee):
    """Sub-version of _Po2 used for CopenhagenProbabilities"""
    d = self.high_orbit_energy - self.low_orbit_energy
    return np.sin(((Ee - d/2) * np.pi) / 5) * 0.5 + 0.5

def __Sigma__(self,P):
    """Sub-version of Sigma used for CopenhagenProbabilities"""
    s = -1 if self.energy_level > self.low_orbit_energy else 1
    Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    po2 = __Po2__(self,Ee)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    self.energy_level = collapse

def __rSigma__(self,P):
    """Sub-version of _Sigma used for CopenhagenProbabilities"""
    s = -1 if self.energy_level > self.low_orbit_energy else 1
    return self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s

def __Gamma__(self,P):
    """Sub-version of Gamma used for CopenhagenProbabilities"""
    s = 1 if self.energy_level > self.low_orbit_energy else -1
    Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    po2 = __Po2__(self,Ee)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    self.energy_level = collapse

def __Omega__(self,P2):
    """Sub-version of Omega used for CopenhagenProbabilities"""
    Ee2 = ((self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)) * __rSigma__(P2,1)
    po2 = __Po2__(self,Ee2)
    collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
    P2.energy_level = collapse

def CopenhagenProbabilities(mm = MEASUREMENT_MODE_EV,iterations = 100):
    """Simple to use function to compute regular probabilities for the given QC system like you can in the old regular
       QC algorithm. Not finished""" #TODO !!!
    global FLAG_RECORD_HISTORY
    if FLAG_RECORD_HISTORY:
        FLAG_RECORD_HISTORY = False
        eVs = []
        for i,qubit in enumerate(QUBITS):
            eVs.append(qubit.energy_level)
            QUBITS[i].energy_level = qubit.low_orbit_energy
        low = np.array([0 for i in range(len(QUBITS))])
        high = np.array([0 for i in range(len(QUBITS))])
        for i in range(iterations):
            for action in GLOBAL_HISTORY:
                if len(action) == 3:
                    action[0](action[1],action[2])
                else:
                    action[0](action[1],QUBITS[action[2]])
            for i, q in enumerate(QUBITS):
                if q.energy_level == q.low_orbit_energy:
                    low[i] += 1
                else:
                    high[i] += 1
                    q.energy_level = q.low_orbit_energy
        low = low / float(iterations)
        high = high / float(iterations)
        qubit_low_orbitals = [q2.low_orbit_energy for q2 in QUBITS]
        qubit_high_orbitals = [q3.high_orbit_energy for q3 in QUBITS]
        FLAG_RECORD_HISTORY = True
        return np.add(np.multiply(low,qubit_low_orbitals),np.multiply(high,qubit_high_orbitals)) * 0.5 if mm == MEASUREMENT_MODE_EV else high
    print(f"{bcolors.FAIL + bcolors.BOLD}ERROR: Cannot compute Copenhagen Probabilities! Missing history! Consider enabling FLAG_RECORD_HISTORY!{bcolors.ENDC}")
    exit()

class DIP_Qubit_Model:
    """
       **TL;DR**

       DIP = Deterministic Ionizing Particle / (Electron jumping between orbitals)

       **Brief explanation of the system**

       It is a model conceptualised from the ground up as a separate quantum computing system
       to allow for a simple mathematical model to describe all useful phenomenons in the QC
       field. Such as entanglement and superposition. Which all work without the need of huge
       state vectors or matrices. This allows for greater speeds and performance to simulate
       quantum systems thousands or even millions of times bigger than anything we have simulated
       before with just a very tiny fraction of the computational power of previous algorithms.
       
       This is a project created by **OctaCore** in July 2024 - Present and is in active development (ofc)
       This project is also a proof of concept and not a well developed technology (yet), however i do hope
       it will be able to change the world for the better. As of the time of writing this there hasn't
       been a paper that has been published on this subject."""
    def __init__(self,index,mm = MEASUREMENT_MODE_EV):
        global FLAG_INITIALIZED
        self.index = index
        self.low_orbit_energy = -10 # eV
        self.energy_level = self.low_orbit_energy
        self.high_orbit_energy = -5 # eV      
        self.measurement_mode = mm
        self.history = [] # TODO
        if not FLAG_INITIALIZED and FLAG_WARNING:
            print(f"{bcolors.WARNING + bcolors.BOLD}Warning!: Printing of any particle counts as measurement and will collapse any superpostion!{bcolors.ENDC}")
            # print(f"{bcolors.BOLD}Consider using the CopenhagenProbabilities method to compute and print the approximate probabilities!{bcolors.ENDC}")
            FLAG_INITIALIZED = True
    def _Po2(self,Ee):
        """Computes the probability of any given energy state, especially inbetween. Unrealistic.
           Used for implmenting collapsing of the qubits."""
        d = self.high_orbit_energy - self.low_orbit_energy
        return np.sin(((Ee - d/2) * np.pi) / 5) * 0.5 + 0.5
    def _Sigma(self,P):
        """Low level version of Sigma. Returns the energy level before collapsing. Unrealistic. 
           Used for implementing Omega."""
        s = -1 if self.energy_level > self.low_orbit_energy else 1
        return self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
    def Sigma(self,P):
        """Allows for easy superposition manipulation in relation to the 1 (down or in this case up) state. 
           !! Applying multiple of these gates in series multiplies their probabilities rather than adding 
           the energy being sent."""
        s = -1 if self.energy_level > self.low_orbit_energy else 1
        Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
        po2 = self._Po2(Ee)
        collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
        self.energy_level = collapse
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Sigma__,self,P])
    def Omega(self,P2):
        """Acts as the CNOT gate and entangles qubit states."""
        Ee2 = ((self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)) * P2._Sigma(1)
        po2 = self._Po2(Ee2)
        collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
        P2.energy_level = collapse
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Omega__,self,P2.index,None])
    def Gamma(self,P):
        """Allows for easy superposition manipulation in relation to the 0 (up or in this case down) state. 
           !! Applying multiple of these gates in series multiplies their probabilities rather than adding 
           the energy being sent."""
        s = 1 if self.energy_level > self.low_orbit_energy else -1
        Ee = self.energy_level + P * (self.high_orbit_energy - self.low_orbit_energy) * s
        po2 = self._Po2(Ee)
        collapse = np.random.choice([self.low_orbit_energy,self.high_orbit_energy],p=[1 - abs(po2),abs(po2)])
        self.energy_level = collapse
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY.append([__Gamma__,self,P])
    def Measure(self):
        """Measures and collapses the value of the given qubit class."""
        global GLOBAL_HISTORY
        if FLAG_RECORD_HISTORY: GLOBAL_HISTORY = []
        return self.energy_level if self.measurement_mode == MEASUREMENT_MODE_EV else (self.energy_level - self.low_orbit_energy) / (self.high_orbit_energy - self.low_orbit_energy)

    def __str__(self):
        return bcolors.OKCYAN + str(self.Measure()) + bcolors.ENDC

QUBITS = [DIP_Qubit_Model(x,MEASUREMENT_MODE_BIN) for x in range(QUBIT_NUMBER)]
