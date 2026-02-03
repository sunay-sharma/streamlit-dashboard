import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ================== PAGE CONFIG ==================
st.set_page_config(
    page_title="Professor-Friendly Dashboard",
    layout="wide"
)

# ================== CUSTOM CSS ==================
st.markdown("""
<style>
body { background-color: #0E1117; color: white; }
h1, h2, h3 { color: #00FFAA; }
div[data-testid="metric-container"] {
    background-color: #1f2937;
    border-radius: 12px;
    padding: 15px;
    box-shadow: 0px 0px 8px #00ffaa;
}
</style>
""", unsafe_allow_html=True)

# ================== TITLE ==================
st.title("📊 Advanced Interactive Dashboard")
st.markdown("**Easy-to-use and visual dashboard for data exploration**")

# ================== SIDEBAR ==================
st.sidebar.header("⚙️ Controls")
uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.sidebar.subheader("🔎 Filters")

    # ================== CATEGORICAL FILTER ==================
    categorical_cols = df.select_dtypes(include=["object"]).columns
    selected_category_col = None
    if len(categorical_cols) > 0:
        selected_category_col = st.sidebar.selectbox(
            "Select a categorical column to filter",
            categorical_cols
        )
        selected_categories = st.sidebar.multiselect(
            "Select values for filter",
            df[selected_category_col].unique()
        )
        if selected_categories:
            df = df[df[selected_category_col].isin(selected_categories)]

    # ================== NUMERIC FILTER ==================
    numeric_cols = df.select_dtypes(include=["int64", "float64"]).columns
    selected_num_col = None
    if len(numeric_cols) > 0:
        selected_num_col = st.sidebar.selectbox(
            "Select numeric column for analysis",
            numeric_cols
        )
        min_val = float(df[selected_num_col].min())
        max_val = float(df[selected_num_col].max())
        range_vals = st.sidebar.slider(
            f"Filter {selected_num_col} range",
            min_val, max_val, (min_val, max_val)
        )
        df = df[(df[selected_num_col] >= range_vals[0]) & (df[selected_num_col] <= range_vals[1])]

    # ================== KPI CARDS ==================
    st.subheader("📌 Key Metrics")
    k1, k2, k3 = st.columns(3)
    k1.metric("Total Rows", df.shape[0])
    k2.metric("Total Columns", df.shape[1])
    k3.metric("Missing Values", df.isnull().sum().sum())

    # ================== DATA PREVIEW ==================
    st.subheader("🔍 Dataset Preview")
    st.dataframe(df.head(20))

    # ================== SUMMARY ==================
    st.subheader("📈 Statistical Summary")
    st.write(df.describe())

    # ================== VISUALIZATIONS ==================
    st.subheader("📊 Visual Analytics")

    if selected_num_col:
        col1, col2 = st.columns(2)

        # Histogram
        with col1:
            st.markdown(f"### 📊 Histogram of {selected_num_col}")
            fig, ax = plt.subplots()
            sns.histplot(df[selected_num_col], bins=25, kde=True, ax=ax, color="#00FFAA")
            ax.set_xlabel(selected_num_col)
            ax.set_ylabel("Frequency")
            st.pyplot(fig)

        # Boxplot
        with col2:
            st.markdown(f"### 📦 Boxplot of {selected_num_col}")
            fig, ax = plt.subplots()
            sns.boxplot(x=df[selected_num_col], ax=ax, color="#FF5733")
            st.pyplot(fig)

        # Line Chart
        st.markdown(f"### 📉 Line Chart of {selected_num_col}")
        st.line_chart(df[selected_num_col])

        # Scatter Plot with categorical color
        if selected_category_col:
            st.markdown(f"### 🔹 Scatter Plot of {selected_num_col} by {selected_category_col}")
            fig, ax = plt.subplots()
            sns.scatterplot(
                data=df,
                x=selected_num_col,
                y=selected_num_col,  # for demo, plot column vs itself
                hue=selected_category_col,
                palette="bright",
                ax=ax
            )
            st.pyplot(fig)

    # ================== ADDITIONAL GRAPH ==================
    if len(categorical_cols) > 0:
        cat_col_for_bar = st.selectbox(
            "Select categorical column for bar chart",
            categorical_cols
        )
        st.markdown(f"### 📊 Count Plot of {cat_col_for_bar}")
        fig, ax = plt.subplots()
        sns.countplot(x=cat_col_for_bar, data=df, palette="Set2", ax=ax)
        st.pyplot(fig)

else:
    st.info("⬅️ Upload your CSV file in the sidebar to explore your data")
