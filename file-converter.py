from fileinput import fileno
from numbers import Number
import streamlit as st # type: ignore
import pandas as pd # type: ignore
from io import BytesIO

st.set_page_config(page_title="File Converter", layout="wide")
st.title("File Converter & cleaner")
st.write("This app is designed to convert csv or excel files ,clean data and convert format.")
files = st.file_uploader("upload csv or excel files", type=["csv", "xlsx"], accept_multiple_files=True)

if files : 
    for file in files :
        ext = file.name.split(".")[-1]
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)
        
        st.subheader(f"{file.name} - preview")
        st.dataframe(df.head())
        
        if st.checkbox(f"remove duplicates in {file.name}"):
            df=df.drop_duplicates()
            st.success("Duplicates removed")
            st.dataframe(df.head())
            
            if st.checkbox(f"Fill Missing Values in {file.name}"):
                df.fillna(df.select_dtypes(include=["number"]).mean(), inplace=True)
                st.success("Missing values filled")
                st.dataframe(df.head())
                
            selected_columns = st.multiselect(f"Select columns in {file.name}", df.columns,default=df.columns)
            df = df[selected_columns]
            st.dataframe(df.head())
                
            if st.checkbox(f"Show Chart in {file.name}")and not df.select_dtypes(include="number").empty:
                    st.bar_chart(df.select_dtypes(include="number").iloc[:,:2])
                    
                    format_choice = st.radio(f"conver in {file.name} to:", ["csv", "excel"],key=file.name)
                    if st.button(f"Download {file.name} as {format_choice}"):
                        output = BytesIO()
                        if format_choice == "csv":
                            df.to_csv(output, index=False)
                            mine = "text/csv"
                            new_name=file.name.replace(ext, "csv")
                        else:
                            df.to_excel(output, index=False, engine="openpyxl")
                            mine = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                            new_name = file.name.replace(ext, "xlsx")
                            
                            output.seek(0)
                            st.download_button(new_name, data=output, mime=mine)
                            st.success("Processing Complete!")
                       
                    
                
                
              



