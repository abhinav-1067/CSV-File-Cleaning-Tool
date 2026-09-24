import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt



## "CSV FILE CLEANING TOOL" heading code-
st.header('CSV FILE CLEANING TOOL')
st.write('Upload your CSV file, explore the data, clean it and download the improved version.')


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
            selected_data = file[selected_col]

            if pd.api.types.is_numeric_dtype(selected_data):
                st.write("Min:", selected_data.min())
                st.write("Max:", selected_data.max())
                st.write("Mean:", selected_data.mean())
                st.write("Median:", selected_data.median())

            else:
                st.write("Unique values:", selected_data.nunique())
                st.write("Most frequent:", selected_data.mode()[0] if not selected_data.mode().empty else "N/A")


# Cleaning Options-
if uploaded_file is not None:
    with st.container(border=True):
        st.subheader('CLEANING OPTIONS.')

        #---------------------------
        # CheckBoxes Here-
        #---------------------------

        # 1. Removing Missing Values-
        remove_missing = st.checkbox('Removing Missing Values')

        # 2. Fill Missing Values-
        col7, col8 = st.columns(2)
        with col7:
            fill_na = st.checkbox('Fill Missing Values')
            if fill_na:
                with col8:
                    method = st.selectbox('Method',['Mean','Zeros','Median/Mode'])

        # 3. Remove Duplicate Values-
        remove_dupli = st.checkbox('Remove Duplicates')

        # 4. Convert datatype-
        col9, col10 = st.columns(2)
        with col9:
            convert_dtype = st.checkbox('Convert Datatype')
        with col10:
            if convert_dtype:
                data_type = st.text_input('Enter Data-Type')
        
        # 5. Change column name-
        col11, col12 = st.columns(2)
        with col11:
            change_col = st.checkbox('Change Column Name')
        if change_col:
            with col12:
                selected_name = st.text_input("Enter New Name")

        #----------------------------------
        # ADDING APPLY BUTTON-
        #----------------------------------
        apply_button = st.button('APPLY CLEANING')

        if apply_button:

            cleaned_file = file.copy()
            # Removing Missing Values-
            if remove_missing:
                cleaned_file = cleaned_file.dropna(subset=[selected_col])

            # Fill Missing Values-
            if fill_na:
                selected_data = cleaned_file[selected_col]
                if method=="Mean":
                    if pd.api.types.is_numeric_dtype(selected_data):
                        cleaned_file[selected_col] = selected_data.fillna(selected_data.mean())
                    else:
                        st.warning("Mean can only be used with numeric columns.")
                elif method=="Zeros":
                    if pd.api.types.is_numeric_dtype(selected_data):
                        cleaned_file[selected_col] = cleaned_file[selected_col].fillna(0)
                    else:
                        st.warning("Zeros can only be used with numeric columns")
                elif method=="Median/Mode":
                    if cleaned_file[selected_col].dtype=='object':
                        cleaned_file[selected_col] = cleaned_file[selected_col].fillna(cleaned_file[selected_col].mode()[0])
                    else:
                        cleaned_file[selected_col] = cleaned_file[selected_col].fillna(cleaned_file[selected_col].median())
                else:
                    pass

            # Remove Duplicates-
            if remove_dupli:
                cleaned_file = cleaned_file.drop_duplicates(subset=[selected_col])

            # Convert Datatype-
            if convert_dtype and data_type:
                cleaned_file[selected_col] = cleaned_file[selected_col].astype(data_type)

            # Changing Column Name-
            if change_col:
                cleaned_file = cleaned_file.rename(columns={selected_col: selected_name})

            #-------------------------
            # SAVE CLEANED DATAFRAME
            #-------------------------
            st.session_state.cleaned_file = cleaned_file
            st.success("CLEANING APPLIED SUCCESSFULLY")

            #---------------------------
            # DOWNLOAD CLEANED FILE
            #---------------------------
            if "cleaned_file" in st.session_state:
                cleaned_csv = st.session_state.cleaned_file.to_csv(
                    index=False
                )

            st.download_button(
                label='DOWNLOAD CLEANED CSV',
                data=cleaned_csv,
                file_name='cleaned_data.csv',
                mime= 'text/csv'
            )