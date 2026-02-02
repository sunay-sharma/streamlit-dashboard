import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Streamlit Dashboard", layout="wide")

st.title("Data Analytics Dashboard")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.subheader("Summary Statistics")
    st.write(df.describe())

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(numeric_cols) > 0:
        col = st.selectbox("Select column", numeric_cols)

        fig, ax = plt.subplots()
        ax.hist(df[col], bins=20)
        ax.set_title(f"Distribution of {col}")
        st.pyplot(fig)
else:
    st.info("Please upload a CSV file")

