from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator


# ---------------------------------------------------
# QUANTUM RISK ANALYSIS
# ---------------------------------------------------

def quantum_risk_analysis(
    risk_score,
    amount,
    recipient_type,
    location_risk
):

    # Create quantum circuit

    qc = QuantumCircuit(1, 1)

    # ---------------------------------------------------
    # HIGH ANOMALY BEHAVIOR
    # ---------------------------------------------------

    if (
        risk_score >= 70
        or amount > 500000
        or recipient_type == "New Recipient"
        or location_risk == "High-Risk Region"
    ):

        # Strong anomaly state
        qc.x(0)

    # ---------------------------------------------------
    # MEDIUM ANOMALY BEHAVIOR
    # ---------------------------------------------------

    elif risk_score >= 40:

        # Quantum uncertainty state
        qc.h(0)

    # ---------------------------------------------------
    # LOW ANOMALY BEHAVIOR
    # ---------------------------------------------------

    else:

        # Keep default |0> state
        pass

    # ---------------------------------------------------
    # MEASUREMENT
    # ---------------------------------------------------

    qc.measure(0, 0)

    # ---------------------------------------------------
    # RUN QUANTUM SIMULATION
    # ---------------------------------------------------

    simulator = AerSimulator()

    job = simulator.run(qc, shots=100)

    result = job.result()

    counts = result.get_counts()

    return counts