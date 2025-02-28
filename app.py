import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Page configuration
st.set_page_config(page_title="Data Sweeper", layout='wide', initial_sidebar_state='expanded')

# Sidebar for user input and file upload
with st.sidebar:
    st.title("🔍 Data Sweeper")
    st.markdown("---")
    user_name = st.text_input("👤 Your Name")
    uploaded_files = st.file_uploader("📄 Upload Files (CSV/Excel):", type=["csv", "xlsx"], accept_multiple_files=True)
    if user_name:
        st.success(f"Welcome, {user_name}!")

# Main Page Title
st.title("✨ Data Sweeper")
st.write("Effortlessly clean, visualize, and convert your data files.")
st.markdown("---")

if uploaded_files:
    st.subheader(f"📌 Uploaded Files by {user_name}")

    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()
        
        # Read file
        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error(f"❌ Unsupported file type: {file_ext}")
            continue

        st.markdown(f"### 📄 {file.name}")
        st.info(f"**File Size:** {file.size / 1024:.2f} KB")
        st.dataframe(df, height=300)
        
        # Data Cleaning Options
        with st.expander(f"🧹 Data Cleaning for {file.name}"):
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Remove Duplicates", key=f"duplicates_{file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicates Removed")
            with col2:
                if st.button(f"Fill Missing Values", key=f"missing_{file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing Values Filled")

        # Column Selection
        with st.expander(f"📌 Select Columns"):
            selected_columns = st.multiselect("Choose Columns", df.columns, default=df.columns, key=f"columns_{file.name}")
            df = df[selected_columns]

        # Data Visualization
        with st.expander(f"📊 Data Visualization"):
            if st.checkbox(f"Show Bar Chart", key=f"chart_{file.name}"):
                st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # File Conversion
        with st.expander(f"🔄 Convert File"):
            conversion_type = st.radio("Convert To:", ["CSV", "Excel"], key=f"convert_{file.name}")
            if st.button(f"Convert", key=f"download_{file.name}"):
                buffer = BytesIO()
                if conversion_type == "CSV":
                    df.to_csv(buffer, index=False)
                    file_name = file.name.replace(file_ext, ".csv")
                    mime_type = "text/csv"
                elif conversion_type == "Excel":
                    df.to_excel(buffer, index=False, engine='openpyxl')
                    file_name = file.name.replace(file_ext, ".xlsx")
                    mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                buffer.seek(0)
                st.download_button(label=f"⬇️ Download {conversion_type}", data=buffer, file_name=file_name, mime=mime_type)

st.success("🚀 All files processed successfully!")