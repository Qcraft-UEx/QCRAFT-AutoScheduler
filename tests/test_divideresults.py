import unittest
from autoscheduler import _divideResults

class TestDivideResults(unittest.TestCase):

    def test_divide_results_ibm(self):
        # 2 users, one with the first qubit (0) and the other with the rest (10, 11). The first one has 0:5000 and the second 10:2500 and 11:5000
        counts = {'010': 2500, '110': 2500} 
        shots = [2500,2500]
        provider='ibm' # aws just changes the format of the results, left to right
        qb = [1,2]
        users = [1,2]
        circuit_name = ['circuit1','circuit2']
        results = _divideResults._divideResults(counts, shots, provider, qb, users, circuit_name)
        self.assertEqual(results, [{(1, 'circuit1'):{'0':5000}}, {(2, 'circuit2'):{'01':2500, '11':2500}}])

    def test_divide_results_aws(self):
        # 2 users, one with the first qubit (0, 1) and the other with the rest (10). The first one has 0:2500 and 1:2500 and the second 10:5000
        counts = {'010': 2500, '110': 2500} 
        shots = [2500,2500]
        provider='aws' # aws just changes the format of the results, left to right
        qb = [1,2]
        users = [1,2]
        circuit_name = ['circuit1','circuit2']
        results = _divideResults._divideResults(counts, shots, provider, qb, users, circuit_name)
        self.assertEqual(results, [{(1, 'circuit1'):{'0':2500, '1':2500}}, {(2, 'circuit2'):{'01':5000}}])

if __name__ == '__main__':
    unittest.main()