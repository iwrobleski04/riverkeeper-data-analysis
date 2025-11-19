import streamlit as st
import pandas as pd
import numpy as np
import json
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from modules.data_analysis import *

st.set_page_config(
    page_title="Donor Analytics",
    page_icon="📊",
)

def run():

    st.markdown("<h1 style='text-align: center;'>Donor Analytics</h1>", unsafe_allow_html=True)

    # connecting to google sheets 
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds_dict = json.loads(st.secrets["google_service_account"]["creds_json"])
    creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
    gc = gspread.authorize(creds)

    # opening sheet
    sheet_name = "Riverkeeper_Donors"
    sh = gc.open(sheet_name)
    worksheet = sh.sheet1

    # load data from sheet and clean
    data = worksheet.get_all_records()
    data = pd.DataFrame(data)
    clean(data)

    page = st.sidebar.radio(
        "Select a Category of Analytics:",
        [
            "Basic Statistics",
            "Active/Inactive Donors",
            "Top Donors",
            "Frequent Donors",
            "Statistics by Location",
            "Statistics by Time"
        ]
    )

    if page == "Basic Statistics":
        st.markdown("<h3 style='text-align: center;'>Basic Statistics</h3>", unsafe_allow_html=True)
        # KPIs, summary tables

    elif page == "Active/Inactive Donors":
        st.markdown("<h3 style='text-align: center;'>Active/Inactive Donors</h3>", unsafe_allow_html=True)
        # Charts...

    elif page == "Top Donors":
        st.markdown("<h3 style='text-align: center;'>Top Donors</h3>", unsafe_allow_html=True)
        # Leaderboards...

    elif page == "Frequent Donors":
        st.markdown("<h3 style='text-align: center;'>Frequent Donors</h3>", unsafe_allow_html=True)
        # Histograms...

    elif page == "Statistics by Location":
        st.markdown("<h3 style='text-align: center;'>Statistics by City and State</h3>", unsafe_allow_html=True)
        # Maps, regional charts...

    elif page == "Statistics by Time":
        st.markdown("<h3 style='text-align: center;'>Statistics by Month and Year</h3>", unsafe_allow_html=True)
        st.text("")
        st.text("")

        st.markdown("<h5 style='text-align: center;'>Donors by Year</h5>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Years and the number of donors whose last donation was in that year.</p>", unsafe_allow_html=True)
        yearly = stats_by_year(data)
        st.bar_chart(yearly)

        st.space(size="small")
        st.markdown("<h5 style='text-align: center;'>Donors by Month</h5>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Months and the number of donors whose last donation was in that month.</p>", unsafe_allow_html=True)
        monthly = stats_by_month(data)
        st.bar_chart(monthly, sort=False)
