import pandas as pd
import streamlit as st
from ydata_profiling import ProfileReport

st.set_page_config(
    page_title="Instant Auto-EDA Dashboard", page_icon="📊", layout="wide"
)

st.title("📊 Instant Auto-EDA & Dataset Dashboard")
st.write(
    "Upload any CSV or Excel file below to automatically generate a complete"
    " analytical dashboard and report."
)

# File uploader supports CSV and Excel
uploaded_file = st.file_uploader(
    "Upload your dataset (.csv, .xlsx)", type=["csv", "xlsx"]
)

if uploaded_file is not None:
  @st.cache_data
  def load_data(file):
    if file.name.endswith(".csv"):
      return pd.read_csv(file)
    else:
      return pd.read_excel(file)

  df = load_data(uploaded_file)

  # Display basic dataset metrics
  st.success("Dataset successfully loaded!")
  
  col1, col2, col3 = st.columns(3)
  col1.metric("Total Rows", df.shape[0])
  col2.metric("Total Columns", df.shape[1])
  col3.metric("Missing Values", df.isna().sum().sum())

  # Preview raw data
  with st.expander("🔍 Preview Raw Dataset"):
    st.dataframe(df.head(50), use_container_width=True)

  # Generate Automated Profiling Report
  st.subheader("📈 Automated Deep-Dive Dashboard")
  with st.spinner("Generating comprehensive dashboard insights..."):
    # Create the profiling report
    pr = ProfileReport(df, explorative=True, minimal=True)
    report_html = pr.to_html()
    
    # Render the HTML report inside Streamlit safely
    st.components.v1.html(report_html, height=1000, scrolling=True)

else:
  st.info("👆 Upload a dataset file above to instantly generate your dashboard.")
