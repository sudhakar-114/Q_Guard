# Q-Guard Final Corrected app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import joblib
from docx import Document
from quantum_module import quantum_risk_analysis

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="Q-Guard",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------
# LOAD MODEL
# ---------------------------------------------------

model = joblib.load("fraud_detection_model.pkl")

# ---------------------------------------------------
# SESSION STORAGE
# ---------------------------------------------------

if "transaction_history" not in st.session_state:
    st.session_state.transaction_history = []

# ---------------------------------------------------
# CUSTOM CSS
# ---------------------------------------------------

st.markdown("""
<style>

body {
    background-color: #0B1120;
}

.main {
    background-color: #0B1120;
    color: white;
}
header {

    background-color: #DBEAFE !important;
}

[data-testid="stHeader"] {

    background-color: #DBEAFE;
}

[data-testid="stToolbar"] {

    right: 2rem;
}

.stTabs [data-baseweb="tab-list"] {

    background-color: #DBEAFE;

    border-radius: 12px;

    padding: 5px;
}

.stTabs [data-baseweb="tab"] {

    color: #1E3A8A;

    font-weight: bold;
}

h1, h2, h3, h4 {
    color: white;
}

[data-testid="stSidebar"] {

    background-color: #DBEAFE;
}

.stButton>button {
    background: linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color: white;

    border-radius: 12px;

    height: 3em;

    width: 100%;

    font-size: 16px;

    border: none;

    font-weight: bold;
}

.stButton>button:hover {

    background: linear-gradient(
        90deg,
        #1D4ED8,
        #6D28D9
    );

    color: white;
}

[data-testid="metric-container"] {

    background-color: #111827;

    border: 1px solid #1F2937;

    padding: 15px;

    border-radius: 15px;

    box-shadow: 0px 0px 15px rgba(
        37,
        99,
        235,
        0.2
    );
}

.stDataFrame {

    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "🔍 Fraud Detection",
        "📊 Analytics"
    ]
)
# ---------------------------------------------------
# HOME PAGE
# ---------------------------------------------------

if menu == "🏠 Home":

    st.markdown(
        """
        <div style="
            background: linear-gradient(
                135deg,
                #DBEAFE,
                #BFDBFE,
                #93C5FD
            );
            padding:60px;
            border-radius:30px;
            text-align:center;
            margin-top:80px;
            box-shadow:0px 6px 25px rgba(
                59,
                130,
                246,
                0.25
            );
        ">
            <h1 style="
                color:#1E3A8A;
                font-size:75px;
                margin-bottom:10px;
            ">
                🛡️ Q-Guard
            </h1>
            <h3 style="
                color:#2563EB;
                margin-bottom:20px;
            ">
                AI-Powered Financial Fraud Detection
            </h3>
            <p style="
                color:#374151;
                font-size:20px;
            ">
                Detect suspicious financial transactions
                instantly using Machine Learning.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------------------------------------------
# FRAUD DETECTION PAGE
# ---------------------------------------------------

elif menu == "🔍 Fraud Detection":

    st.header("🔍 Transaction Analysis")

    tab1, tab2 = st.tabs(
        ["Manual Input", "Upload Excel File"]
    )

    # ---------------------------------------------------
    # MANUAL INPUT TAB
    # ---------------------------------------------------

    with tab1:

        col1, col2 = st.columns(2)

        with col1:

            amount = st.number_input(
                "Transaction Amount",
                min_value=0.0,
                value=1000.0
            )

            transaction_type = st.selectbox(
                "Transaction Type",
                [
                    "PAYMENT",
                    "TRANSFER",
                    "CASH_OUT",
                    "DEBIT"
                ]
            )

            transaction_time = st.slider(
                "Transaction Time",
                0,
                23,
                12
            )

        with col2:

            device_type = st.selectbox(
                "Device Type",
                [
                    "Mobile Banking",
                    "Web Banking",
                    "ATM"
                ]
            )

            recipient_type = st.selectbox(
                "Recipient Type",
                [
                    "Saved Recipient",
                    "New Recipient"
                ]
            )

            location_risk = st.selectbox(
                "Location Risk",
                [
                    "Trusted Location",
                    "Unknown Location",
                    "High-Risk Region"
                ]
            )

        st.markdown("---")

        # ---------------------------------------------------
        # ANALYZE BUTTON
        # ---------------------------------------------------

        if st.button("⚡ Analyze Transaction"):

            # -----------------------------------
            # ENCODING MAPS
            # -----------------------------------

            type_mapping = {
                "PAYMENT": 0,
                "TRANSFER": 1,
                "CASH_OUT": 2,
                "DEBIT": 3
            }

            location_mapping = {
                "Trusted Location": 0,
                "Unknown Location": 1,
                "High-Risk Region": 2
            }

            recipient_mapping = {
                "Saved Recipient": 0,
                "New Recipient": 1
            }

            # -----------------------------------
            # CREATE INPUT DATA
            # -----------------------------------

            input_data = pd.DataFrame([{
                "amount": amount,
                "type": type_mapping[transaction_type],
                "transaction_time": transaction_time,
                "location_risk": location_mapping[location_risk],
                "recipient_status": recipient_mapping[recipient_type]
            }])

            # -----------------------------------
            # MODEL PREDICTION
            # -----------------------------------

            prediction = model.predict(input_data)[0]

            # -----------------------------------
            # RISK SCORE LOGIC
            # -----------------------------------

            risk_score = 15

            if amount > 50000:
                risk_score += 30

            if transaction_type in ["TRANSFER", "CASH_OUT"]:
                risk_score += 20

            if transaction_time >= 22 or transaction_time <= 4:
                risk_score += 15

            if recipient_type == "New Recipient":
                risk_score += 10

            if location_risk == "High-Risk Region":
                risk_score += 20

            risk_score = min(risk_score, 100)

            # -----------------------------------
            # FRAUD RESULT
            # -----------------------------------

            st.markdown("---")

            if prediction == 1:

                risk_score = max(risk_score, 85)

                st.error("⚠️ HIGH RISK FRAUD DETECTED")

                risk_level = "HIGH"

            else:

                risk_score = min(risk_score, 35)

                st.success("✅ Transaction Appears Safe")

                risk_level = "LOW"

            # -----------------------------------
            # RISK SCORE
            # -----------------------------------

            st.metric(
                "Fraud Risk Score",
                f"{risk_score}%"
            )

            st.progress(risk_score)

            # -----------------------------------
            # RISK LEVEL
            # -----------------------------------

            if risk_level == "HIGH":
                st.error("Risk Level: HIGH")
            else:
                st.success("Risk Level: LOW")

            # -----------------------------------
            # RISK FACTORS
            # -----------------------------------

            st.markdown("### 🚨 Risk Factors")

            reasons = []

            if amount > 50000:
                reasons.append(
                    "Large transaction amount detected"
                )

            if transaction_type in [
                "TRANSFER",
                "CASH_OUT"
            ]:
                reasons.append(
                    "High-risk transaction type"
                )

            if transaction_time >= 22 or transaction_time <= 4:
                reasons.append(
                    "Suspicious late-night transaction"
                )

            if recipient_type == "New Recipient":
                reasons.append(
                    "Transfer to new recipient"
                )

            if location_risk == "High-Risk Region":
                reasons.append(
                    "Transaction from high-risk region"
                )

            if len(reasons) == 0:
                reasons.append(
                    "No major fraud indicators detected"
                )

            for reason in reasons:
                st.write(f"• {reason}")

            # -----------------------------------
            # QUANTUM ANALYSIS
            # -----------------------------------

            with st.expander("⚛️ Quantum Analysis"):

                quantum_result = quantum_risk_analysis(
                    risk_score,
                    amount,
                    recipient_type,
                    location_risk
                )

                st.info(
                    "Hybrid quantum-classical fraud analysis completed successfully."
                )

                st.write("### Quantum Measurement Results")

                st.write(quantum_result)

                ones = quantum_result.get("1", 0)
                zeros = quantum_result.get("0", 0)

                total = ones + zeros

                anomaly_probability = (
                    ones / total
                ) * 100

                st.write(
                    f"Quantum Anomaly Probability: {anomaly_probability:.1f}%"
                )

                if anomaly_probability >= 75:

                    st.error(
                        "Quantum system detected HIGH anomaly behavior."
                    )

                    quantum_status = "HIGH"

                elif anomaly_probability >= 45:

                    st.warning(
                        "Quantum system detected MODERATE anomaly behavior."
                    )

                    quantum_status = "MODERATE"

                else:

                    st.success(
                        "Quantum system indicates NORMAL transaction behavior."
                    )

                    quantum_status = "NORMAL"

                st.write(
                    "Qiskit-powered quantum simulation executed successfully."
                )

            # -----------------------------------
            # SAVE TRANSACTION HISTORY
            # -----------------------------------

            transaction_record = {

                "Amount": amount,

                "Transaction_Type": transaction_type,

                "Risk_Score": risk_score,

                "Risk_Level": risk_level,

                "Prediction": (
                    "FRAUD"
                    if risk_level == "HIGH"
                    else "SAFE"
                ),

                "Quantum_Probability": round(
                    anomaly_probability,
                    2
                ),

                "Quantum_Status": quantum_status
            }

            st.session_state.transaction_history.append(
                transaction_record
            )

    # ---------------------------------------------------
    # FILE UPLOAD TAB
    # ---------------------------------------------------

    with tab2:

        st.subheader("📁 Upload Transaction File")

        uploaded_file = st.file_uploader(
            "Upload CSV or Excel File",
            type=["csv", "xlsx"]
        )

        if uploaded_file is not None:

            # -----------------------------------
            # READ FILE
            # -----------------------------------

            if uploaded_file.name.endswith(".csv"):

                df_upload = pd.read_csv(
                    uploaded_file
                )

            else:

                df_upload = pd.read_excel(
                    uploaded_file
                )

            st.write("### Uploaded Transactions")

            st.dataframe(df_upload.head())

            # -----------------------------------
            # SAVE ORIGINAL VALUES
            # -----------------------------------

            original_transaction_types = df_upload[
                "type"
            ].copy()

            # -----------------------------------
            # ENCODING MAPS
            # -----------------------------------

            type_mapping = {
                "PAYMENT": 0,
                "TRANSFER": 1,
                "CASH_OUT": 2,
                "DEBIT": 3
            }

            location_mapping = {
                "Trusted Location": 0,
                "Unknown Location": 1,
                "High-Risk Region": 2
            }

            recipient_mapping = {
                "Saved Recipient": 0,
                "New Recipient": 1
            }

            # -----------------------------------
            # ENCODE COLUMNS
            # -----------------------------------

            df_upload["type"] = df_upload[
                "type"
            ].map(type_mapping)

            df_upload["location_risk"] = df_upload[
                "location_risk"
            ].map(location_mapping)

            df_upload["recipient_status"] = df_upload[
                "recipient_status"
            ].map(recipient_mapping)

            # -----------------------------------
            # SELECT MODEL FEATURES
            # -----------------------------------

            model_input = df_upload[[
                "amount",
                "type",
                "transaction_time",
                "location_risk",
                "recipient_status"
            ]]

            # -----------------------------------
            # ML PREDICTION
            # -----------------------------------

            predictions = model.predict(
                model_input
            )

            # -----------------------------------
            # RISK SCORE LOGIC
            # -----------------------------------

            risk_scores = []

            quantum_probabilities = []

            quantum_statuses = []

            for index, row in df_upload.iterrows():

                score = 15

                if row["amount"] > 500000:
                    score += 30

                if row["type"] in [1, 2]:
                    score += 20

                if (
                    row["transaction_time"] >= 22
                    or row["transaction_time"] <= 4
                ):
                    score += 15

                if row["recipient_status"] == 1:
                    score += 10

                if row["location_risk"] == 2:
                    score += 20

                score = min(score, 100)

                # -----------------------------------
                # QUANTUM ANALYSIS
                # -----------------------------------

                    # -----------------------------------
                    # SMART QUANTUM ANALYSIS
                    # -----------------------------------

                if score >= 50:

                        quantum_result = (
                            quantum_risk_analysis(

                                score,

                                row["amount"],

                                "New Recipient"
                                if row["recipient_status"] == 1
                                else "Saved Recipient",

                                "High-Risk Region"
                                if row["location_risk"] == 2
                                else "Trusted Location"
                            )
                        )

                        ones = quantum_result.get(
                            "1",
                            0
                        )

                        zeros = quantum_result.get(
                            "0",
                            0
                        )

                        total = ones + zeros

                        quantum_probability = (
                            ones / total
                        ) * 100

                else:

                        # Skip heavy quantum simulation
                        # for low-risk transactions

                        quantum_probability = 10

                    # -----------------------------------
                    # SAVE QUANTUM RESULTS
                    # -----------------------------------

                quantum_probabilities.append(
                        round(
                            quantum_probability,
                            2
                        )
                    )

                    # -----------------------------------
                    # QUANTUM STATUS
                    # -----------------------------------

                if quantum_probability >= 75:

                        quantum_statuses.append(
                            "HIGH"
                        )

                elif quantum_probability >= 45:

                        quantum_statuses.append(
                            "MODERATE"
                        )

                else:

                        quantum_statuses.append(
                            "NORMAL"
                        )

                    # -----------------------------------
                    # SAVE RISK SCORE
                    # -----------------------------------

                risk_scores.append(score)

            # -----------------------------------
            # ADD ANALYSIS RESULTS
            # -----------------------------------

            df_upload["Risk_Score"] = risk_scores

            df_upload[
                "Quantum_Probability"
            ] = quantum_probabilities

            df_upload[
                "Quantum_Status"
            ] = quantum_statuses

            # -----------------------------------
            # FINAL FRAUD DECISION
            # -----------------------------------

            final_predictions = []

            for i in range(len(predictions)):

                if (
                    predictions[i] == 1
                    or risk_scores[i] >= 70
                    or quantum_statuses[i] == "HIGH"
                ):

                    final_predictions.append(
                        "FRAUD"
                    )

                else:

                    final_predictions.append(
                        "SAFE"
                    )

            df_upload[
                "Fraud_Prediction"
            ] = final_predictions

            # -----------------------------------
            # DISPLAY RESULTS
            # -----------------------------------

            st.write("### Fraud Analysis Results")

            st.dataframe(
    df_upload,
    use_container_width=True
)

            # -----------------------------------
            # FRAUD COUNT
            # -----------------------------------

            fraud_count = (
                df_upload[
                    "Fraud_Prediction"
                ] == "FRAUD"
            ).sum()

            st.metric(
                "Detected Fraud Transactions",
                fraud_count
            )

            # -----------------------------------
            # SAVE BULK TRANSACTIONS
            # -----------------------------------

            for index, row in df_upload.iterrows():

                transaction_record = {

                    "Amount": row["amount"],

                    "Transaction_Type": (
                        original_transaction_types.iloc[
                            index
                        ]
                    ),

                    "Risk_Score": row[
                        "Risk_Score"
                    ],

                    "Risk_Level": (
                        "HIGH"
                        if row["Risk_Score"] >= 70
                        else "LOW"
                    ),

                    "Prediction": row[
                        "Fraud_Prediction"
                    ],

                    "Quantum_Probability": row[
                        "Quantum_Probability"
                    ],

                    "Quantum_Status": row[
                        "Quantum_Status"
                    ]
                }

                st.session_state.transaction_history.append(
                    transaction_record
                )

# ---------------------------------------------------
# ANALYTICS PAGE
# ---------------------------------------------------

elif menu == "📊 Analytics":

    st.header("📊 Live Fraud Analytics Dashboard")

    if len(st.session_state.transaction_history) == 0:

        st.warning(
            "No transactions analyzed yet."
        )

    else:

        history_df = pd.DataFrame(
            st.session_state.transaction_history
        )

        total_transactions = len(history_df)

        fraud_count = len(
            history_df[
                history_df["Prediction"] == "FRAUD"
            ]
        )

        fraud_percentage = (
            fraud_count / total_transactions
        ) * 100

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Total Transactions",
                total_transactions
            )

        with col2:
            st.metric(
                "Fraud Detected",
                fraud_count
            )

        with col3:
            st.metric(
                "Fraud Percentage",
                f"{fraud_percentage:.2f}%"
            )

        st.markdown("---")

        # -----------------------------------
        # RECENT TRANSACTIONS
        # -----------------------------------

        st.subheader("🧾 Recent Transactions")

        st.dataframe(history_df)

        st.markdown("---")

        # -----------------------------------
        # FRAUD DISTRIBUTION
        # -----------------------------------

        st.subheader("🚨 Fraud Distribution")

        fraud_distribution = history_df[
            "Prediction"
        ].value_counts().reset_index()

        fraud_distribution.columns = [
            "Category",
            "Count"
        ]

        fig1 = px.pie(
            fraud_distribution,
            names="Category",
            values="Count",
            title="Fraud vs Safe Transactions"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------------
        # RISK LEVEL DISTRIBUTION
        # -----------------------------------

        st.subheader("⚠️ Risk Level Distribution")

        risk_distribution = history_df[
            "Risk_Level"
        ].value_counts().reset_index()

        risk_distribution.columns = [
            "Risk_Level",
            "Count"
        ]

        fig2 = px.pie(
            risk_distribution,
            names="Risk_Level",
            values="Count",
            title="Risk Level Analysis"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

        st.markdown("---")

        # -----------------------------------
        # QUANTUM DISTRIBUTION
        # -----------------------------------

        st.subheader("⚛️ Quantum Anomaly Distribution")

        quantum_distribution = history_df[
            "Quantum_Status"
        ].value_counts().reset_index()

        quantum_distribution.columns = [
            "Quantum_Status",
            "Count"
        ]

        fig3 = px.pie(
            quantum_distribution,
            names="Quantum_Status",
            values="Count",
            title="Quantum Anomaly Analysis"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

        # -----------------------------------
        # DOWNLOAD WORD REPORT
        # -----------------------------------

        st.markdown("---")

        st.subheader("📄 Download Fraud Report")

        if st.button("Generate Word Report"):

            doc = Document()

            # -----------------------------------
            # TITLE
            # -----------------------------------

            doc.add_heading(
                "Q-Guard Fraud Analysis Report",
                level=1
            )

            # -----------------------------------
            # SUMMARY
            # -----------------------------------

            doc.add_heading(
                "Summary",
                level=2
            )

            doc.add_paragraph(
                f"Total Transactions: {total_transactions}"
            )

            doc.add_paragraph(
                f"Fraud Detected: {fraud_count}"
            )

            doc.add_paragraph(
                f"Fraud Percentage: {fraud_percentage:.2f}%"
            )

            # -----------------------------------
            # TRANSACTION DETAILS
            # -----------------------------------

            doc.add_heading(
                "Transaction Details",
                level=2
            )

            for index, row in history_df.iterrows():

                doc.add_paragraph(
                    f"""
Transaction {index + 1}

Amount: {row['Amount']}
Transaction Type: {row['Transaction_Type']}
Risk Score: {row['Risk_Score']}
Risk Level: {row['Risk_Level']}
Prediction: {row['Prediction']}
Quantum Probability: {row.get('Quantum_Probability', 'N/A')}
Quantum Status: {row.get('Quantum_Status', 'N/A')}
                    """
                )

            # -----------------------------------
            # SAVE DOCUMENT
            # -----------------------------------

            report_path = (
                "QGuard_Fraud_Report.docx"
            )

            doc.save(report_path)

            # -----------------------------------
            # DOWNLOAD BUTTON
            # -----------------------------------

            with open(report_path, "rb") as file:

                st.download_button(
                    label="📥 Download Word Report",
                    data=file,
                    file_name="QGuard_Fraud_Report.docx",
                    mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                )

