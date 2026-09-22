import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



## "CSV FILE CLEANING TOOL" heading code-
st.header('CSV FILE CLEANING TOOL')
st.write('Upload your CSV file, explore the data, clean it and download the improved version.')

def file_upload(uploaded_file):
    uploaded_file = st.file_uploader('Upload Your CSV File',
                                        type=["csv"])
    file = pd.read_csv(uploaded_file)
    return file

# Adding File Uploading Section-
def section1():
    with st.container(border=True):
        st.subheader('1. Upload DataSet')
        uploaded_file = st.file_uploader('Upload Your CSV File',
                                    type=["csv"])

        if uploaded_file is not None:
            st.success('File Uploaded Successfully')
            with st.container(border=True):
                st.text('file name:')
                st.write(uploaded_file.name)
            # Reading Uploaded CSV File-
            file = pd.read_csv(uploaded_file)

section1()

# Now Show DataSets Overview-
def section2(uploaded_file):
    col1, col2, col3, col4 = st.columns(4)
    uploaded_file = file_upload()
    file = pd.read_csv(uploaded_file)
    rows = file.shape[0]
    with col1:
        with st.container(border=True):
            st.metric('Rows:',
                      rows)
            

section2()