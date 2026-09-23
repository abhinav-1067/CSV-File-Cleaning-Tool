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
    if uploaded_file is not None:
        return uploaded_file

# Adding File Uploading Section-
st.subheader('1. UPLOAD FILE.')
with st.container(border=True):
    uploaded_file = st.file_uploader("Upload CSV",
                                    type=['csv'])
    if uploaded_file is not None:
        st.success('File Uploaded Successfully')
        with st.container(border=True):
            st.text('file name:')
            st.write(uploaded_file.name)
        # Reading Uploaded CSV File-
        file = pd.read_csv(uploaded_file)

# Now Show DataSets Overview-
st.subheader('2. DATASET OVERVIEW.')
with st.container(border=True):
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        with st.container(border=True):
                st.write('Rows:')
                if uploaded_file is not None:
                    st.write(file.shape[0])

    with col2:
        with st.container(border=True):
            st.write('Columns:')
            if uploaded_file is not None:
                st.write(file.shape[1])

    with col3:
        with st.container(border=True):
            st.write('Missing Values:')
            if uploaded_file is not None:
                st.write(file.isnull().sum().sum())

    with col4:
        with st.container(border=True):
            st.write('Duplicates:')
            if uploaded_file is not None:
                st.write(file.duplicated().sum())

#Adding DataSet Preview-
col5, col6 = st.columns(2)
with col5:
    if uploaded_file is not None:
        st.write('DATASET PREVIEW.')
        st.dataframe(file.head())

with col6:
    if uploaded_file is not None:
        with st.container(border=True):
            st.write('SELECT COLUMN.')
            selected_col = st.selectbox('Select Column',
                                        file.columns)
            st.write('Data Type: ',file[selected_col].dtype)
            st.write('Missing Values: ',file[selected_col].isnull().sum())
            st.write('Unique Values: ',file[selected_col].nunique())
            st.write('Duplicate Values: ',file[selected_col].duplicated().sum())
            st.write('Min: ',file[selected_col].min())
            st.write('Max: ',file[selected_col].max())

# Cleaning Options-
if uploaded_file is not None:
    with st.container(border=True):
        st.subheader('CLEANING OPTIONS.')

        # Removing Missing Values-
        remove_missing = st.checkbox('Removing Missing Values')
        if remove_missing:
            file = file.dropna(subset=[selected_col])

        # Fill Missing Values-
        col7, col8 = st.columns(2)
        with col7:
            fill_na = st.checkbox('Fill Missing Values')
        with col8:
            method = st.selectbox('Method',['Mean','Zeros','Median','Mode'])
        if fill_na:
            if method=="Mean":
                