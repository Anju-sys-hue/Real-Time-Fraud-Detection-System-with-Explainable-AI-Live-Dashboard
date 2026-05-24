# =====================================================
# REAL-TIME FRAUD DETECTION SYSTEM
# WITH EXPLAINABLE AI & LIVE DASHBOARD
# =====================================================

import streamlit as st
import pandas as pd
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Fraud Detection Dashboard",
    page_icon="💳",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# LOAD DATA
# =====================================================

df = pd.read_csv("sample_data.csv")

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""

<style>

/* Main Background */

.stApp {

    background:
    linear-gradient(
    135deg,
    #0f172a,
    #111827,
    #1e293b
    );

    color: white;
}

/* Sidebar */

section[data-testid="stSidebar"] {

    background:
    linear-gradient(
    180deg,
    #1e3c72,
    #2a5298
    );
}

/* Sidebar Text */

section[data-testid="stSidebar"] * {

    color: white !important;
}

/* KPI Cards */

.metric-card {

    background:
    rgba(255,255,255,0.08);

    backdrop-filter:
    blur(14px);

    border:
    1px solid rgba(255,255,255,0.15);

    border-radius: 20px;

    padding: 22px;

    text-align: center;

    box-shadow:
    0px 4px 20px rgba(0,0,0,0.3);

    transition: 0.3s;

    margin-bottom: 15px;
}

.metric-card:hover {

    transform: scale(1.03);
}

/* Headers */

h1, h2, h3, h4 {

    color: white;
}

/* Paragraph */

p {

    color: #d1d5db;
}

/* Dataframe */

[data-testid="stDataFrame"] {

    border-radius: 15px;

    overflow: hidden;
}

/* Buttons */

.stButton>button {

    background:
    linear-gradient(
    90deg,
    #4f46e5,
    #06b6d4
    );

    color: white;

    border: none;

    border-radius: 10px;

    padding: 10px 20px;

    font-weight: bold;
}

</style>

""", unsafe_allow_html=True)

# =====================================================
# TITLE
# =====================================================

st.markdown("""

<h1 style='
text-align: center;
font-size: 48px;
font-weight: 800;
background: linear-gradient(
90deg,
#4f46e5,
#06b6d4,
#9333ea
);
-webkit-background-clip: text;
-webkit-text-fill-color: transparent;
margin-bottom: 10px;
'>

Real-Time Fraud Detection System
with Explainable AI & Live Dashboard

</h1>

""", unsafe_allow_html=True)

st.markdown("""

<p style='
text-align: center;
font-size: 18px;
color: #cbd5e1;
margin-bottom: 30px;
'>

AI-Powered Fraud Analytics Platform for
Risk Segmentation, Fraud Monitoring,
and SHAP Explainability

</p>

""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.title("📌 Navigation")

page = st.sidebar.radio(

    "Go To",

    [
        "Overview",
        "Transaction Explorer",
        "SHAP Explainability"
    ]
)

# =====================================================
# OVERVIEW PAGE
# =====================================================

if page == "Overview":

    st.header("📊 Executive Overview")

    # =================================================
    # KPI VALUES
    # =================================================

    total_transactions = len(df)

    total_fraud = int(
        df["ActualFraud"].sum()
    )

    fraud_rate = (
        total_fraud / total_transactions
    ) * 100

    avg_amt = df[
        "TransactionAmt"
    ].mean()

    critical_count = len(

        df[
            df["RiskTier"] ==
            "Critical Risk"
        ]
    )

    # =================================================
    # KPI CARDS
    # =================================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.markdown(f"""
        <div class="metric-card">
            <h4>Total Transactions</h4>
            <h2>{total_transactions:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col2:

        st.markdown(f"""
        <div class="metric-card">
            <h4>Total Fraud</h4>
            <h2>{total_fraud:,}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col3:

        st.markdown(f"""
        <div class="metric-card">
            <h4>Fraud Rate</h4>
            <h2>{fraud_rate:.2f}%</h2>
        </div>
        """, unsafe_allow_html=True)

    with col4:

        st.markdown(f"""
        <div class="metric-card">
            <h4>Avg Transaction</h4>
            <h2>${avg_amt:.2f}</h2>
        </div>
        """, unsafe_allow_html=True)

    with col5:

        st.markdown(f"""
        <div class="metric-card">
            <h4>Critical Risk</h4>
            <h2>{critical_count}</h2>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # =================================================
    # CHARTS ROW 1
    # =================================================

    col1, col2 = st.columns(2)

    # RISK TIER DONUT

    with col1:

        risk_counts = df[
            "RiskTier"
        ].value_counts().reset_index()

        risk_counts.columns = [
            "RiskTier",
            "Count"
        ]

        fig1 = px.pie(

            risk_counts,

            names="RiskTier",

            values="Count",

            hole=0.5,

            title="Risk Tier Distribution",

            color="RiskTier",

            color_discrete_map={

                "Critical Risk":"red",

                "Suspicious":"orange",

                "Clear":"green"
            }
        )

        fig1.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # FRAUD RATE BY HOUR

    with col2:

        fraud_hour = df.groupby(
            "HourOfDay"
        )["ActualFraud"].mean().reset_index()

        fig2 = px.line(

            fraud_hour,

            x="HourOfDay",

            y="ActualFraud",

            markers=True,

            title="Fraud Rate by Hour"
        )

        fig2.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    # =================================================
    # CHARTS ROW 2
    # =================================================

    col3, col4 = st.columns(2)

    # TRANSACTION AMOUNT DISTRIBUTION

    with col3:

        fig3 = px.histogram(

            df,

            x="TransactionAmt",

            nbins=50,

            title="Transaction Amount Distribution"
        )

        fig3.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig3,
            use_container_width=True
        )

    # DEVICE TYPE DISTRIBUTION

    with col4:

        device_counts = df.groupby(

            ["RiskTier", "DeviceType"]

        ).size().reset_index(name="Count")

        fig4 = px.bar(

            device_counts,

            x="RiskTier",

            y="Count",

            color="DeviceType",

            barmode="group",

            title="Device Type Distribution"
        )

        fig4.update_layout(
            template="plotly_dark"
        )

        st.plotly_chart(
            fig4,
            use_container_width=True
        )

    # =================================================
    # BONUS SCATTER PLOT
    # =================================================

    st.subheader("📌 Fraud Probability Analysis")

    fig5 = px.scatter(

        df.sample(3000),

        x="TransactionAmt",

        y="HourOfDay",

        color="FraudProbability",

        hover_data=[

            "RiskTier",
            "DeviceType"
        ],

        title="Transaction Amount vs Hour Of Day"
    )

    fig5.update_layout(
        template="plotly_dark"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

    # =================================================
    # BUSINESS INSIGHTS
    # =================================================

    st.markdown("---")

    st.subheader("📌 Key Fraud Insights")

    st.info("""

    • High transaction amounts demonstrated elevated fraud probability.

    • Fraudulent behavior increased during unusual transaction hours.

    • Critical Risk transactions showed stronger behavioral anomalies.

    • Mobile and Unknown devices appeared more frequently in suspicious activity.

    • SHAP analysis identified TransactionAmt, DeviceRisk,
      and HourOfDay as major fraud indicators.

    • LightGBM achieved the strongest fraud detection performance.

    """)

# =====================================================
# TRANSACTION EXPLORER
# =====================================================

elif page == "Transaction Explorer":

    st.header("🔍 Transaction Explorer")

    # =================================================
    # SIDEBAR FILTERS
    # =================================================

    risk_filter = st.sidebar.multiselect(

        "Select Risk Tier",

        df["RiskTier"].unique(),

        default=df["RiskTier"].unique()
    )

    device_filter = st.sidebar.multiselect(

        "Select Device Type",

        df["DeviceType"].unique(),

        default=df["DeviceType"].unique()
    )

    filtered_df = df[

        (df["RiskTier"].isin(risk_filter)) &

        (df["DeviceType"].isin(device_filter))
    ]

    # =================================================
    # SEARCH TRANSACTION
    # =================================================

    search_id = st.text_input(
        "Search Transaction ID"
    )

    if search_id:

        filtered_df = filtered_df[

            filtered_df[
                "TransactionID"
            ].astype(str).str.contains(search_id)
        ]

    # =================================================
    # IMPORTANT COLUMNS
    # =================================================

    important_cols = [

        "TransactionID",
        "TransactionAmt",
        "HourOfDay",
        "DeviceType",
        "DeviceRisk",
        "FraudProbability",
        "RiskTier",
        "ActualFraud"

    ]

    available_cols = [

        col for col in important_cols
        if col in filtered_df.columns
    ]

    st.dataframe(

        filtered_df[
            available_cols
        ].head(100),

        use_container_width=True
    )

    # =================================================
    # LIVE RISK SCORE
    # =================================================

    st.markdown("---")

    st.subheader("🎯 Live Risk Score")

    selected_id = st.selectbox(

        "Select Transaction ID",

        df.sort_values(

            by="FraudProbability",

            ascending=False

        )["TransactionID"]
    )

    selected_row = df[
        df["TransactionID"] == selected_id
    ]

    probability = selected_row[
        "FraudProbability"
    ].values[0]

    risk = selected_row[
        "RiskTier"
    ].values[0]

    actual = selected_row[
        "ActualFraud"
    ].values[0]

    st.success(
        f"Fraud Probability: {probability:.4f}"
    )

    st.warning(
        f"Risk Tier: {risk}"
    )

    st.error(
        f"Actual Fraud Label: {actual}"
    )

    st.write("### Transaction Details")

    st.dataframe(

        selected_row[[

            "TransactionID",
            "TransactionAmt",
            "HourOfDay",
            "DeviceType",
            "DeviceRisk",
            "FraudProbability",
            "RiskTier",
            "ActualFraud"

        ]],

        use_container_width=True
    )

# =====================================================
# SHAP EXPLAINABILITY PAGE
# =====================================================

elif page == "SHAP Explainability":

    st.header("🧠 SHAP Explainability")

    # SHAP SUMMARY

    st.subheader("Global SHAP Summary Plot")

    st.image(
        "shap_summary.png",
        use_container_width=True
    )

    st.markdown("---")

    # WATERFALL PLOTS

    st.subheader("SHAP Waterfall Explanations")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.image(
            "waterfall_fraud.png",
            caption="Confirmed Fraud Case"
        )

    with col2:

        st.image(
            "waterfall_borderline.png",
            caption="Borderline Case"
        )

    with col3:

        st.image(
            "waterfall_legit.png",
            caption="Legitimate Transaction"
        )

    st.markdown("---")

    # SHAP INTERPRETATION

    st.subheader("📌 SHAP Interpretation")

    st.info("""

    SHAP values explain how each feature influenced fraud prediction.

    Positive SHAP values increase fraud probability.

    Negative SHAP values decrease fraud probability.

    Top Fraud Signals:
    • TransactionAmt
    • DeviceRisk
    • HourOfDay
    • Behavioral transaction patterns

    """)

    st.markdown("---")

    # PLAIN ENGLISH EXPLANATION

    st.subheader("💡 Plain-English Fraud Explanation")

    st.success("""

    Fraudulent transactions were primarily associated with unusually high transaction amounts,
    suspicious transaction timing patterns,
    and risky device behavior.

    The AI model combined these behavioral indicators to identify
    high-risk transactions with strong predictive confidence.

    """)