import unittest
from autoscheduler import _translator

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.common_values = { # testing different encodings with all available gates
            'quirk': 'https://algassert.com/quirk#circuit={"cols":[["H","Y","Z^¼","X^½"],["X"],["Z",1,"Y^½","X^-½"],["•","X"],["•","Z"],["Swap","Swap"],[1,1,1,"X^¼"],["Z^½","Z^-½"],["Y","•","•"],["Z","•","•","•"],[1,1,1,"X^-¼"],["Y^¼","Y^-¼","Z^-¼","Y^-½"],["Measure","Measure","Measure","Measure"]]}',
            'quirk_exported': 'https://algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22H%22%2C%22Y%22%2C%22Z%5E%C2%BC%22%2C%22X%5E%C2%BD%22%5D%2C%5B%22X%22%5D%2C%5B%22Z%22%2C1%2C%22Y%5E%C2%BD%22%2C%22X%5E-%C2%BD%22%5D%2C%5B%22%E2%80%A2%22%2C%22X%22%5D%2C%5B%22%E2%80%A2%22%2C%22Z%22%5D%2C%5B%22Swap%22%2C%22Swap%22%5D%2C%5B1%2C1%2C1%2C%22X%5E%C2%BC%22%5D%2C%5B%22Z%5E%C2%BD%22%2C%22Z%5E-%C2%BD%22%5D%2C%5B%22Y%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%5D%2C%5B%22Z%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%2C%22%E2%80%A2%22%5D%2C%5B1%2C1%2C1%2C%22X%5E-%C2%BC%22%5D%2C%5B%22Y%5E%C2%BC%22%2C%22Y%5E-%C2%BC%22%2C%22Z%5E-%C2%BC%22%2C%22Y%5E-%C2%BD%22%5D%2C%5B%22Measure%22%2C%22Measure%22%2C%22Measure%22%2C%22Measure%22%5D%5D%7D',
            'quirk_copied': 'https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22,%22Y%22,%22Z^%C2%BC%22,%22X^%C2%BD%22],[%22X%22],[%22Z%22,1,%22Y^%C2%BD%22,%22X^-%C2%BD%22],[%22%E2%80%A2%22,%22X%22],[%22%E2%80%A2%22,%22Z%22],[%22Swap%22,%22Swap%22],[1,1,1,%22X^%C2%BC%22],[%22Z^%C2%BD%22,%22Z^-%C2%BD%22],[%22Y%22,%22%E2%80%A2%22,%22%E2%80%A2%22],[%22Z%22,%22%E2%80%A2%22,%22%E2%80%A2%22,%22%E2%80%A2%22],[1,1,1,%22X^-%C2%BC%22],[%22Y^%C2%BC%22,%22Y^-%C2%BC%22,%22Z^-%C2%BC%22,%22Y^-%C2%BD%22],[%22Measure%22,%22Measure%22,%22Measure%22,%22Measure%22]]}',
            'ibm_circuit': """circuit.h(qreg_q[3])\ncircuit.y(qreg_q[4])\ncircuit.t(qreg_q[5])\ncircuit.rx(np.pi/2, qreg_q[6])\ncircuit.x(qreg_q[3])\ncircuit.z(qreg_q[3])\ncircuit.ry(np.pi/2, qreg_q[5])\ncircuit.rx(-np.pi/2, qreg_q[6])\nmc_x_gate = MCMT(XGate(), 1, 1)\ncircuit.append(mc_x_gate, [qreg_q[3], qreg_q[4]])\nmc_z_gate = MCMT(ZGate(), 1, 1)\ncircuit.append(mc_z_gate, [qreg_q[3], qreg_q[4]])\ncircuit.swap(qreg_q[3], qreg_q[4])\ncircuit.rx(np.pi/4, qreg_q[6])\ncircuit.s(qreg_q[3])\ncircuit.sdg(qreg_q[4])\nmc_y_gate = MCMT(YGate(), 2, 1)\ncircuit.append(mc_y_gate, [qreg_q[4], qreg_q[5], qreg_q[3]])\nmc_z_gate = MCMT(ZGate(), 3, 1)\ncircuit.append(mc_z_gate, [qreg_q[4], qreg_q[5], qreg_q[6], qreg_q[3]])\ncircuit.rx(-np.pi/4, qreg_q[6])\ncircuit.ry(np.pi/4, qreg_q[3])\ncircuit.ry(-np.pi/4, qreg_q[4])\ncircuit.tdg(qreg_q[5])\ncircuit.ry(-np.pi/2, qreg_q[6])\ncircuit.measure(qreg_q[3], creg_c[3])\ncircuit.measure(qreg_q[4], creg_c[4])\ncircuit.measure(qreg_q[5], creg_c[5])\ncircuit.measure(qreg_q[6], creg_c[6])""",
            'aws_circuit': """circuit.h(3)\ncircuit.y(4)\ncircuit.t(5)\ncircuit.rx(6, np.pi/2)\ncircuit.x(3)\ncircuit.z(3)\ncircuit.ry(5, np.pi/2)\ncircuit.rx(6, -np.pi/2)\ncircuit.cnot(3, 4)\ncircuit.cz(3, 4)\ncircuit.swap(3, 4)\ncircuit.rx(6, np.pi/4)\ncircuit.s(3)\ncircuit.si(4)\ncircuit.cy(4, 3)\ncircuit.cz(4, 3)\ncircuit.rx(6, -np.pi/4)\ncircuit.ry(3, np.pi/4)\ncircuit.ry(4, -np.pi/4)\ncircuit.ti(5)\ncircuit.ry(6, -np.pi/2)"""
        }

    def test_get_ibm_individual(self):
        quirk = self.common_values['quirk']
        translated_circuit = _translator._get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual(self):
        quirk = self.common_values['quirk']
        translated_circuit = _translator._get_aws_individual(quirk, 3)          

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_ibm_individual_exported_quirk_circuit(self):
        quirk = self.common_values['quirk_exported']
        translated_circuit = _translator._get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual_exported_quirk_circuit(self):
        quirk = self.common_values['quirk_exported']
        translated_circuit = _translator._get_aws_individual(quirk, 3)

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_ibm_individual_copied_quirk_circuit_url(self):
        quirk = self.common_values['quirk_copied']
        translated_circuit = _translator._get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual_copied_quirk_circuit_url(self):
        quirk = self.common_values['quirk_copied']
        translated_circuit = _translator._get_aws_individual(quirk, 3)

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)
        

if __name__ == '__main__':
    unittest.main()