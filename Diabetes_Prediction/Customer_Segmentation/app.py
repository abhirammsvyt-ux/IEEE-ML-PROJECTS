import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.cluster import AgglomerativeClustering

st.title("Customer Segmentation Dashboard")

st.write("""
This dashboard segments customers using the K-Means Clustering algorithm
based on Annual Income and Spending Score.
""")

uploaded_file = st.file_uploader(
    "Upload Customer CSV",
    type=["csv"]
)

if uploaded_file:

    # Read Dataset
    df = pd.read_csv(uploaded_file)

    # Dataset Validation
    required_columns = [
        'Annual Income (k$)',
        'Spending Score (1-100)'
    ]

    if not all(col in df.columns for col in required_columns):

        st.error("""
        Invalid Dataset!

        Please upload a customer dataset containing:

        • Annual Income (k$)
        • Spending Score (1-100)

        The model was trained using the Mall Customer Segmentation Dataset.
        """)

        st.stop()

    # Total Customers
    st.metric("Total Customers", len(df))

    # Dataset Preview
    st.subheader("Dataset Preview")
    st.write(df.head())

    # Features
    X = df[['Annual Income (k$)',
            'Spending Score (1-100)']]

    # Load K-Means Model
    model = joblib.load("models/kmeans_model.pkl")

    # Predict Clusters
    df['Cluster'] = model.predict(X)

    # Clustered Customers
    st.subheader("Clustered Customers")
    st.write(df.head())

    # -------------------------
    # K-MEANS VISUALIZATION
    # -------------------------

    st.subheader("Customer Segments (K-Means)")

    fig, ax = plt.subplots(figsize=(8,5))

    ax.scatter(
        df['Annual Income (k$)'],
        df['Spending Score (1-100)'],
        c=df['Cluster']
    )

    ax.set_xlabel("Annual Income")
    ax.set_ylabel("Spending Score")
    ax.set_title("K-Means Customer Segmentation")

    st.pyplot(fig)

    # Cluster Count
    st.subheader("Cluster Count")

    st.bar_chart(
        df['Cluster'].value_counts()
    )

    # Income & Spending Analysis
    st.subheader("Income and Spending Analysis")

    cluster_summary = df.groupby('Cluster')[[
        'Annual Income (k$)',
        'Spending Score (1-100)'
    ]].mean().round(2)

    st.write(cluster_summary)

    # -------------------------
    # BUSINESS INSIGHTS
    # -------------------------

    st.subheader("Business Insights")

    st.success(
        "Cluster 1 : High Income, High Spending (Premium Customers)"
    )

    st.info(
        "Cluster 0 : Average Income, Average Spending"
    )

    st.warning(
        "Cluster 3 : High Income, Low Spending"
    )

    st.info(
        "Cluster 2 : Low Income, High Spending"
    )

    st.error(
        "Cluster 4 : Low Income, Low Spending"
    )

    # -------------------------
    # BONUS MODEL
    # -------------------------

    st.subheader("Bonus Model: Hierarchical Clustering")

    st.write("""
    Hierarchical Clustering was implemented as an additional clustering technique.
    The results are compared with K-Means Clustering.
    """)

    # Hierarchical Clustering

    hc = AgglomerativeClustering(n_clusters=5)

    df['HC_Cluster'] = hc.fit_predict(X)

    # Hierarchical Graph

    st.subheader("Hierarchical Clustering Visualization")

    fig2, ax2 = plt.subplots(figsize=(8,5))

    ax2.scatter(
        df['Annual Income (k$)'],
        df['Spending Score (1-100)'],
        c=df['HC_Cluster']
    )

    ax2.set_xlabel("Annual Income")
    ax2.set_ylabel("Spending Score")
    ax2.set_title("Hierarchical Clustering")

    st.pyplot(fig2)

    # Hierarchical Summary

    st.subheader("Hierarchical Cluster Analysis")

    hc_summary = df.groupby('HC_Cluster')[[
        'Annual Income (k$)',
        'Spending Score (1-100)'
    ]].mean().round(2)

    st.write(hc_summary)

    # -------------------------
    # COMPARISON TABLE
    # -------------------------

    st.subheader("K-Means vs Hierarchical Comparison")

    comparison_values = pd.DataFrame({
        "K-Means Income":
            cluster_summary['Annual Income (k$)'].values,

        "Hierarchical Income":
            hc_summary['Annual Income (k$)'].values,

        "K-Means Spending":
            cluster_summary['Spending Score (1-100)'].values,

        "Hierarchical Spending":
            hc_summary['Spending Score (1-100)'].values
    })

    st.write(comparison_values)

    # -------------------------
    # MODEL COMPARISON
    # -------------------------

    st.subheader("Model Comparison")

    comparison_data = pd.DataFrame({
        "Feature": [
            "Speed",
            "Dendrogram",
            "Large Dataset Handling",
            "Customer Segmentation"
        ],
        "K-Means": [
            "Fast",
            "No",
            "Good",
            "Good"
        ],
        "Hierarchical": [
            "Slower",
            "Yes",
            "Moderate",
            "Good"
        ]
    })

    st.table(comparison_data)