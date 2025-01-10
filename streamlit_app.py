import streamlit as st
import pandas as pd
import re

def clean_column_names(df):
    """Clean column names: lowercase, replace spaces with underscores, remove special characters."""
    df.columns = [
        re.sub(r"[^\w\s]", "", col).strip().lower().replace(" ", "_") for col in df.columns
    ]
    return df

# Streamlit app
st.title("Spreadsheet Cleaner")

# File upload
uploaded_file = st.file_uploader("Upload your spreadsheet (Excel or CSV)", type=["csv", "xlsx"])

if uploaded_file:
    # Read the file
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            # Import openpyxl if not already installed
            try:
                import openpyxl
            except ImportError:
                st.error("The openpyxl library is required to read Excel files. Please install it using 'pip install openpyxl'.")
                st.stop()
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Unsupported file format.")
            st.stop()

        st.subheader("Original File Preview")
        st.write(df)

        # Clean column names
        cleaned_df = clean_column_names(df)

        st.subheader("Cleaned File Preview")
        st.write(cleaned_df)

        # Download cleaned file
        st.download_button(
            label="Download Cleaned File",
            data=cleaned_df.to_csv(index=False).encode("utf-8"),
            file_name="cleaned_file.csv",
            mime="text/csv",
        )
    except Exception as e:
        st.error(f"An error occurred while processing the file: {e}")
