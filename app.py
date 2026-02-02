import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="Creative Data Dashboard", layout="wide")

# ---------- Custom Styling ----------
st.markdown("""
<style>
.main { background-color: #0E1117; }
h1, h2, h3 { color: #00FFAA; }
div[data-testid="metric-container"] {
    background-color: #1f2937;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 0px 10px #00ffaa;
}
</style>
""", unsafe_allow_html=True)

st.title("🚀 Creative Data Analytics Dashboard")
st.markdown("**Interactive dashboard built using Streamlit**")

uploaded_file = st.file_uploader("📂 Upload CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader("📊 Key Metrics")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Rows", df.shape[0])
    c2.metric("Total Columns", df.shape[1])
    c3.metric("Missing Values", df.isnull().sum().sum())

    st.subheader("🔍 Data Preview")
    st.dataframe(df.head(15))

    st.subheader("📈 Summary Statistics")
    st.write(df.describe())

    num_cols = df.select_dtypes(include=["int64", "float64"]).columns

    if len(num_cols) > 0:
        col = st.selectbox("Select numeric column", num_cols)

        fig, ax = plt.subplots()
        sns.histplot(df[col], bins=25, kde=True, ax=ax)
        st.pyplot(fig)

        st.line_chart(df[col])

else:
    st.info("⬆️ Upload a CSV file to begin")
