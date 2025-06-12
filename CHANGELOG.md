## [1.2.1] - 2025-06-12
### Added
- Added new tests for `schedule_and_execute` and other methods on `autoscheduler` class
- Added new classifiers in `pyproject.toml`

## [1.2.0] - 2025-06-10
### Added
- Added compatibility with version 2 of Qiskit, including the if_test conditional operation
- Added new tests for `autoscheduler`

### Fixed
- Solved an error in which `schedule_and_execute` sometimes didn't autoschedule the circuit
- Solved an error in which specifying an index in classical registers were handled as if the entire classical register was specified

## [1.1.1] - 2025-02-26
### Changed
- _code_to_circuit_ibm can now handle correctly circuits using numpy library

## [1.1.0] - 2024-10-31
### Added
- Added compatibility with more gates, including S, T, rotation gates... and multicontrolled gates for both Qiskit and Amazon Braket
- Added new tests for `translator`

### Changed
- Improved internal handling of circuit objects for better compatibility
- Changed Qiskit Runtime primitive backend.run() to the modern V2 primitives

## [1.0.0] - 2024-10-04
### Added
- Increased the Sphinx documentation with `changelog.rst` and `introduction.rst` reStructuredText files
- Added new `MANIFEST.in` file to include `tox.ini`, `CHANGELOG.md`, `examples` folder and `docs` folder to the python distribution
- Added information about the shot optimization on `README.md`
- Now `max_qubits` can be inferred from the machine
- New examples has been added to show the usage of `schedule_and_execute` method
- Added new tests for the inferring qubits functionality

### Changed
- `max_qubits` is now an optional parameter in `schedule` and `schedule_and_execute`. Code from previous versions must be migrated by using `max_qubits=...`
- `machine` is now an optional parameter in `schedule` as it can be used to infer `max_qubits` from the number of qubits of the machine. It is mandatory to use at least one of this two parameters for `schedule` and `schedule_and_execute`
- Enhanced the internal documentation of the `Autoscheduler` class for better clarity on its functionality and to be compatible with Sphinx Napoleon.

## [0.2.0] - 2024-07-15
### Added
- Added Sphinx-based documentation
- Added new tests for `scheduler`

### Changed
- Migrated from `setup.py` to `pyproject.toml` for a more modern and standardized build configuration

## [0.1.5] - 2024-07-11
### Added
- Added new tests for `_divideResults` and `_translator`

### Fixed
- `_code_to_circuit_ibm` can now handle Registers without name, like QuantumRegister(2) or ClassicalRegister(2)

## [0.1.4] - 2024-07-08
### Added
- Added support for Python 3.10, 3.11 and 3.12

## [0.1.3] - 2024-07-05
### Fixed
- `_code_to_circuit_ibm` can now handle c_if operation on every quantum gate
- `_code_to_circuit_ibm` can now handle barrier operation in any form (barrier(), barrier(qreg), barrier(qreg[i], qreg[j],...))

## [0.1.2] - 2024-07-02
### Fixed
- `_analyze_circuit` no longer fails when a GitHub URL circuit have comments in the middle of the line
- `_code_to_circuit_ibm` and `_code_to_circuit_aws` can now handle np and np.pi
