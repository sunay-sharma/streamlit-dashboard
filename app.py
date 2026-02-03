import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Streamlit Data Dashboard",
    layout="wide"
)

st.title("📊 Streamlit Data Visualization Dashboard")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data.csv")

df = load_data()

st.subheader("Dataset Preview")
st.dataframe(df.head())

# -------------------------
# Sidebar
# -------------------------
st.sidebar.header("Filters")
numeric_cols = df.select_dtypes(include="number").columns
selected_col = st.sidebar.selectbox("Select Numeric Column", numeric_cols)

# -------------------------
# KPIs
# -------------------------
st.subheader("Key Metrics")
c1, c2, c3 = st.columns(3)

c1.metric("Mean", f"{df[selected_col].mean():.2f}")
c2.metric("Max", f"{df[selected_col].max():.2f}")
c3.metric("Min", f"{df[selected_col].min():.2f}")

# -------------------------
# Charts
# -------------------------
st.subheader("Visualizations")

col1, col2 = st.columns(2)

with col1:
    fig, ax = plt.subplots()
    ax.plot(df[selected_col])
    ax.set_title(f"Line Chart – {selected_col}")
    st.pyplot(fig)

with col2:
    fig, ax = plt.subplots()
    ax.hist(df[selected_col], bins=20)
    ax.set_title(f"Histogram – {selected_col}")
    st.pyplot(fig)

# -------------------------
# Correlation Heatmap
# -------------------------
st.subheader("Correlation Heatmap")

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(df[numeric_cols].corr(), annot=True, cmap="coolwarm")
st.pyplot(fig)
