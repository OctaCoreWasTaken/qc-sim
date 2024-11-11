import unittest
import qc_sim
import copy

initflag = copy.deepcopy(qc_sim.FLAG_WARNING)
qc_sim.FLAG_WARNING = False

class TestQubit(unittest.TestCase):
    def test_po2(self):
        q = qc_sim.Qubit(0)
        self.assertAlmostEqual(q._Po2(q.high_orbit_energy * 0.5 + q.low_orbit_energy * 0.5),0.5)
    
    def test__sigma(self):
        q = qc_sim.Qubit(0)
        result = q._Sigma(0.5)
        self.assertAlmostEqual(result,(q.high_orbit_energy + q.low_orbit_energy) * 0.5)

    def test_sigma(self):
        result = 0
        iterations = 100
        for i in range(iterations):
            q = qc_sim.Qubit(0)
            q.Sigma(0.5)
            result += q._Po2(q.energy_level) / iterations
        result = round(2 * result - 1)
        self.assertEqual(result,0,"oh hell nah")

    def test_gamma(self):
        result = 0
        iterations = 100
        for i in range(iterations):
            q = qc_sim.Qubit(0)
            q.Gamma(0.5)
            result += q._Po2(q.energy_level) / iterations
        result = round(2 * result - 1)
        self.assertEqual(result,0)

    def test_omega(self):
        q0 = qc_sim.Qubit(0)
        q1 = qc_sim.Qubit(0)
        q0.Sigma(1)
        q0.Omega(q1)
        self.assertAlmostEqual(q1.energy_level,q1.high_orbit_energy)

    def test_measure(self):
        q = qc_sim.Qubit(0)
        q.Sigma(1)
        starting_point = copy.deepcopy(qc_sim.GLOBAL_STARTING_POINT)
        result = q.Measure()
        self.assertNotEqual(starting_point,qc_sim.GLOBAL_STARTING_POINT)
        self.assertEqual(result,q.energy_level)

qc_sim.FLAG_WARNING = initflag