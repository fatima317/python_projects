import streamlit as st
import pandas as pd
import os
from io import BytesIO


# setting up the app
st.set_page_config(page_title="💿 Data Sweeper", layout="wide")

st.markdown("""
    <style>
        .main { background-color: #f9f9f9; }
        h1 { color: #5B2C6F; font-family: 'Segoe UI', sans-serif; text-align: center; }
        .stButton > button {
            background-color: #6C3483;
            color: white;
            border-radius: 10px;
            padding: 0.5em 1em;
            font-weight: bold;
            transition: all 0.3s ease;
        }
            .stDownloadButton > button {
            background-color: #229954;
            color: white;
            border-radius: 10px;
            font-weight: bold;
        }
        .file-preview {
            background-color: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }
            .section-header {
            color: #2E86C1;
            font-size: 1.2rem;
            margin-top: 20px;
            margin-bottom: 10px;
        }
    </style>
""", unsafe_allow_html=True)

st.title("💿 Data Sweeper")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your CSV or Excel files:", type=["csv", "xlsx"], 
accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            # Read CSV file
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            # Read Excel file
            df = pd.read_excel(file)
        else:
            st.error(f"Unsupported file type: {file_ext}")
            continue

        # Display file info
        st.write(f"**File Name:** {file.name}")
        st.write(f"**File Size:** {file.size / 1024}")

        # Show 5 rows of the dataframe
        st.write("Preview the Head of the DataFrame")
        st.dataframe(df.head())

        # Data cleaning options
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button("Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Duplicates removed successfully!")

            with col2:
                if st.button(f"Fill Missing Values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values have been Filled!")

        # Choose specific columns to Keep or Convert
        st.subheader("Select Columns to Convert")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]

        # Visualization options
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualization for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        # Convert to CSV or Excel
        st.subheader("🔄 Convertion Options")
        conversion_type = st.radio(f"Convert {file.name} to:", ("CSV", "Excel"), key=file.name)
        buffer = BytesIO()
        file_name = ""
        mime_type = ""

        if st.button(f"Convert {file.name}"):
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

        # Download the converted file
        st.download_button(
            label=f"Download {file.name} as {conversion_type}",
            data=buffer,
            file_name=file_name,
            mime=mime_type
        )

st.success("🎉 All files processed!")
                    