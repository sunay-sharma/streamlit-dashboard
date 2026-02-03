import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Advanced Data Analytics Dashboard",
    layout="wide"
)

# ================= CUSTOM CSS =================
st.markdown("""
<style>
.main { background-color: #0E1117; }
h1, h2, h3 { color: #00FFAA; }
div[data-testid="metric-container"] {
    background-color: #1f2937;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 0px 8px #00ffaa;
}
</style>
""", unsafe_allow_html=True)

# ================= TITLE =================
st.title("🚀 Advanced Data Analytics Dashboard")
st.markdown("**Interactive Streamlit dashboard with filters and visual analytics**")

# ================= SIDEBAR =================
st.sidebar.header("⚙️ Dashboard Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV File", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    # ================= BASIC FILTER =================
    st.sidebar.subheader("🔎 Data Filters")

    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    categorical_cols = df.select_dtypes(include=["object"]).columns

    # Categorical filter
    if len(categorical_cols) > 0:
        category_col = st.sidebar.selectbox(
            "Filter by category column",
            categorical_cols
        )
        selected_category = st.sidebar.multiselect(
            "Select category values",
            df[category_col].unique()
        )

        if selected_category:
            df = df[df[category_col].isin(selected_category)]

    # ================= KPI METRICS =================
    st.subheader("📊 Key Performance Indicators")

    k1, k2, k3 = st.columns(3)
    k1.metric("Total Rows", df.shape[0])
    k2.metric("Total Columns", df.shape[1])
    k3.metric("Missing Values", df.isnull().sum().sum())

    # ================= DATA PREVIEW =================
    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head(20))

    # ================= SUMMARY =================
    st.subheader("📈 Statistical Summary")
    st.write(df.describe())

    # ================= VISUALIZATIONS =================
    st.subheader("📊 Visual Analysis")

    if len(numeric_cols) > 0:
        selected_num_col = st.selectbox(
            "Select numeric column for analysis",
            numeric_cols
        )

        c1, c2 = st.columns(2)

        # -------- Histogram --------
        with c1:
            st.markdown(f"### 📊 Distribution of {selected_num_col}")
            fig1, ax1 = plt.subplots()
            sns.histplot(df[selected_num_col], bins=30, kde=True, ax=ax1)
            ax1.set_title(f"Histogram of {selected_num_col}")
            ax1.set_xlabel(selected_num_col)
            ax1.set_ylabel("Frequency")
            st.pyplot(fig1)

        # -------- Boxplot --------
        with c2:
            st.markdown(f"### 📦 Boxplot of {selected_num_col}")
            fig2, ax2 = plt.subplots()
            sns.boxplot(x=df[selected_num_col], ax=ax2)
            ax2.set_title(f"Boxplot of {selected_num_col}")
            st.pyplot(fig2)

        # -------- Line Chart --------
        st.markdown(f"### 📉 Trend of {selected_num_col}")
        st.line_chart(df[selected_num_col])

    else:
        st.warning("No numeric columns available for visualization")

else:
    st.info("⬅️ Upload a CSV file using the sidebar to start")
