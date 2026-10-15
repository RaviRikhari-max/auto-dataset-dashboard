import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Instant Dataset Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Instant Dataset Insights Dashboard")
st.write(
    "Upload any CSV or Excel file to instantly view metrics, summary"
    " statistics, missing value breakdowns, and column visualizations."
)

# File uploader
uploaded_file = st.file_uploader(
    "Choose a CSV or Excel file", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  @st.cache_data
  def load_data(file):
    if file.name.endswith(".csv"):
      return pd.read_csv(file)
    else:
      return pd.read_excel(file)

  df = load_data(uploaded_file)

  # Top-level metrics
  st.success("Dataset loaded successfully!")
  col1, col2, col3, col4 = st.columns(4)
  col1.metric("Rows", f"{df.shape[0]:,}")
  col2.metric("Columns", f"{df.shape[1]:,}")
  col3.metric("Missing Cells", f"{df.isna().sum().sum():,}")
  col4.metric("Duplicate Rows", f"{df.duplicated().sum():,}")

  # Tabs for organization
  tab1, tab2, tab3 = st.tabs(
      ["📋 Data Preview", "📊 Summary Statistics", "📈 Quick Charts"]
  )

  with tab1:
    st.subheader("Raw Data Inspector")
    st.dataframe(df, use_container_width=True)

  with tab2:
    st.subheader("Statistical Overview")
    st.dataframe(df.describe(include="all"), use_container_width=True)

    st.subheader("Missing Values per Column")
    missing_df = pd.DataFrame({
        "Missing Count": df.isnull().sum(),
        "Percentage (%)": (df.isnull().mean() * 100).round(2),
    })
    st.dataframe(missing_df[missing_df["Missing Count"] > 0], use_container_width=True)

  with tab3:
    st.subheader("Visualizations")
    numeric_columns = df.select_dtypes(
        include=["float64", "int64"]
    ).columns.tolist()

    if numeric_columns:
      selected_col = st.selectbox(
          "Select a numeric column to view distribution:", numeric_columns
      )
      st.line_chart(df[selected_col])

      st.markdown(f"**Histogram / Values for {selected_col}:**")
      st.bar_chart(df[selected_col].head(50))
    else:
      st.info("No numeric columns found in this dataset for plotting charts.")

else:
  st.info("👆 Upload a dataset file to generate your dashboard insights.")
