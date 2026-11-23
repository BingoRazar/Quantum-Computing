
def apply_oracle(qc, marked_state):
    """
    Flip the phase of the specified marked state.
    """

    n = len(marked_state)

    # Convert the target into the all-ones state.
    # Qiskit displays bitstrings from highest qubit to lowest.
    for qubit in range(n):
        if marked_state[n - 1 - qubit] == "0":
            qc.x(qubit)

    # Multi-controlled Z operation.
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)

    # Undo the X gates.
    for qubit in range(n):
        if marked_state[n - 1 - qubit] == "0":
            qc.x(qubit)
