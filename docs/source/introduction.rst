.. _introduction:

=====================
QCRAFT AutoScheduler
=====================

QCRAFT AutoScheduler is a library that allows users to automatically schedule the execution of their own quantum circuits, improving efficiency and reducing execution times in quantum computing environments.

Purpose
=======

QCRAFT AutoScheduler aims to solve the problem of the increasing cost of quantum tasks by providing a way to decrease the shots needed to obtain the desired results.

Features
========

- **Cost reduction**: QCRAFT AutoScheduler reduces the cost of quantum tasks by reducing the shots of quantum circuits.

Optimizing Quantum Tasks
========================
This library aims for the shot optimization on quantum tasks. Reducing the cost of the circuit on the end-user.

Shot optimization
-----------------
To achieve the shot optimization, the original circuit will be composed multiple time with itself. The more segments, the less shots will be needed to replicate the original circuit.
The total number of shots may differ from the original on a very small scale because the library combines the original circuit multiple times. Depending on the maximum number of qubits, to achieve the desired number of shots and cost reduction the algorithm will create segments equal to the original circuit each with a proportional number of shots, all this on a unique circuit.

**Example:**
Consider a circuit with 2 qubits, requiring 100 shots. If the maximum number of qubits of the new scheduled circuit is 6, the shots will be reduced to 100/(6/2) = 34 in total. Upon uncheduling, the results of each segment of the circuit will be aggregated, resulting on 34*(6/2) = 102 shots in total. Even so, the cost reduction has been achieved because the number of shots has been reduced from 100 to 34.

Getting Started
===============

To get started with QCRAFT AutoScheduler, please proceed to the :ref:`installation` section. The installation guide will help you install the library and its dependencies.
After installing the library, you can proceed to the :ref:`usage` section to learn how to use QCRAFT AutoScheduler in your projects.
