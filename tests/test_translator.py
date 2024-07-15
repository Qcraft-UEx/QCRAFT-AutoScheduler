import unittest
from autoscheduler import _get_aws_individual
from autoscheduler import _get_ibm_individual

class TestTranslator(unittest.TestCase):

    def setUp(self):
        self.common_values = { # testing different encodings with all available gates
            'quirk': 'https://algassert.com/quirk#circuit={"cols":[["H"],["X"],["Z"],["•","X"],["•","Z"],["Swap","Swap"],["Measure", "Measure"]]}',
            'quirk_exported': 'https://algassert.com/quirk#circuit=%7B%22cols%22%3A%5B%5B%22H%22%5D%2C%5B%22X%22%5D%2C%5B%22Z%22%5D%2C%5B%22%E2%80%A2%22%2C%22X%22%5D%2C%5B%22%E2%80%A2%22%2C%22Z%22%5D%2C%5B%22Swap%22%2C%22Swap%22%5D%2C%5B%22Measure%22%2C%22Measure%22%5D%5D%7D',
            'quirk_copied': 'https://algassert.com/quirk#circuit={%22cols%22:[[%22H%22],[%22X%22],[%22Z%22],[%22%E2%80%A2%22,%22X%22],[%22%E2%80%A2%22,%22Z%22],[%22Swap%22,%22Swap%22],[%22Measure%22,%20%22Measure%22]]}',
            'ibm_circuit': """circuit.h(qreg_q[3])\ncircuit.x(qreg_q[3])\ncircuit.z(qreg_q[3])\ncircuit.cx(qreg_q[3], qreg_q[4])\ncircuit.cx(qreg_q[3], qreg_q[4])\ncircuit.swap(qreg_q[3], qreg_q[4])\ncircuit.measure(qreg_q[3], creg_c[3])\ncircuit.measure(qreg_q[4], creg_c[4])""",
            'aws_circuit': """circuit.h(3)\ncircuit.x(3)\ncircuit.z(3)\ncircuit.cnot(3, 4)\ncircuit.cnot(3, 4)\ncircuit.swap(3, 4)"""
        }

    def test_get_ibm_individual(self):
        quirk = self.common_values['quirk']
        translated_circuit = _get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual(self):
        quirk = self.common_values['quirk']
        translated_circuit = _get_aws_individual(quirk, 3)

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_ibm_individual_exported_quirk_circuit(self):
        quirk = self.common_values['quirk_exported']
        translated_circuit = _get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual_exported_quirk_circuit(self):
        quirk = self.common_values['quirk_exported']
        translated_circuit = _get_aws_individual(quirk, 3)

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_ibm_individual_copied_quirk_circuit_url(self):
        quirk = self.common_values['quirk_copied']
        translated_circuit = _get_ibm_individual(quirk, 3)

        circuit = self.common_values['ibm_circuit']

        self.assertEqual(translated_circuit, circuit)

    def test_get_aws_individual_copied_quirk_circuit_url(self):
        quirk = self.common_values['quirk_copied']
        translated_circuit = _get_aws_individual(quirk, 3)

        circuit = self.common_values['aws_circuit']

        self.assertEqual(translated_circuit, circuit)
        

if __name__ == '__main__':
    unittest.main()