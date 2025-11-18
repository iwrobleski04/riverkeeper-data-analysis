import streamlit as st
import pandas as pd
import numpy as np
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from modules.merge_csv import merge_csv

# connecting to google sheets 
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
gc = gspread.authorize(creds)

# opening sheet
sheet_name = "Riverkeeper_Donors"
sh = gc.open(sheet_name)
worksheet = sh.sheet1

# load old data from sheet
data = worksheet.get_all_records()
old_df = pd.DataFrame(data)

st.markdown("<h1 style='text-align: center;'>Dataset Merger</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Upload the new dataset below to merge with the existing dataset.</p>", unsafe_allow_html=True)
st.text("")
st.text("")

# display existing data
st.markdown("<p style='text-align: center;'>Existing Dataset:</p>", unsafe_allow_html=True)
st.dataframe(old_df)

# button to upload new csv
uploaded_file = st.file_uploader("", type="csv")
if uploaded_file:

    # merge datasets
    new_df = pd.read_csv(uploaded_file)
    merged_df, new_rows_df = merge_csv(old_df, new_df, save=False)

    # replace nans with empty strings to avoid error
    merged_df_clean = merged_df.replace([np.inf, -np.inf], np.nan)
    merged_df_clean = merged_df_clean = merged_df_clean.fillna('')

    # update google sheet
    worksheet.clear()
    worksheet.update([merged_df_clean.columns.values.tolist()] + merged_df_clean.values.tolist())

    st.success("Merged CSV saved and updated!")
    st.text("")
    st.text("")

    # display new data
    st.markdown("<p style='text-align: center;'>Merged Dataset:</p>", unsafe_allow_html=True)
    st.dataframe(merged_df)

    csv = merged_df.to_csv(index=False).encode("utf-8")
    new_csv = new_rows_df.to_csv(index=False).encode("utf-8")

    # buttons to save merged data or new rows only
    empty1, col1, col2, empty2 = st.columns([1, 2, 2, 1])
    with col1:
        st.download_button("Download Merged CSV", csv, "merged_data.csv", "text/csv")
    with col2:
        st.download_button("Download New Rows CSV", new_csv, "new_data.csv", "text/csv")
