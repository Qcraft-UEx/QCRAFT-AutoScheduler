## [0.1.4] - 2024-07-08
### Fixed
- Adding support for Python 3.10, 3.11 and 3.12

## [0.1.3] - 2024-07-05
### Fixed
- _code_to_circuit_ibm can now handle c_if operation on every quantum gate
- _code_to_circuit_ibm can now handle barrier operation in any form (barrier(), barrier(qreg), barrier(qreg[i], qreg[j],...))

## [0.1.2] - 2024-07-02
### Fixed
- _analyze_circuit no longer fails when a GitHub URL circuit have comments in the middle of the line
- _code_to_circuit_ibm and _code_to_circuit_aws can now handle np and np.pi
