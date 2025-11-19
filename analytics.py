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
            "Donors by Location",
            "Donors by Time"
        ]
    )

    if page == "Basic Statistics":
        st.markdown("<h2 style='text-align: center;'>Basic Statistics</h2>", unsafe_allow_html=True)
        # KPIs, summary tables

    elif page == "Active/Inactive Donors":
        st.markdown("<h2 style='text-align: center;'>Active/Inactive Donors</h2>", unsafe_allow_html=True)
        # Charts...

    elif page == "Top Donors":
        st.markdown("<h2 style='text-align: center;'>Top Donors</h2>", unsafe_allow_html=True)
        # Leaderboards...

    elif page == "Frequent Donors":
        st.markdown("<h2 style='text-align: center;'>Frequent Donors</h2>", unsafe_allow_html=True)
        # Histograms...

    elif page == "Donors by Location":

        st.markdown("<h2 style='text-align: center;'>Donors by State and City</h2>", unsafe_allow_html=True)
        st.space(size="medium")

        def debug_dataframe(df, max_rows=5):
            st.write("### DataFrame Debug Info")

            # 1. Basic info
            st.write("**Shape:**", df.shape)
            st.write("**Columns:**", list(df.columns))
            st.write("**Index:**", df.index)
            st.write("**Index type:**", type(df.index))
            st.write("**Index names:**", df.index.names)

            # 2. Column types and nulls
            col_info = pd.DataFrame({
                "dtype": df.dtypes,
                "num_missing": df.isna().sum(),
                "unique_values": df.nunique()
            })
            st.write("**Column info:**")
            st.dataframe(col_info)

            # 3. Check for mixed types in each column
            st.write("**Mixed types per column:**")
            mixed_types = {}
            for col in df.columns:
                types = df[col].apply(type).unique()
                if len(types) > 1:
                    mixed_types[col] = types
            st.write(mixed_types if mixed_types else "No mixed types detected")

            # 4. Show first few rows
            st.write("**First few rows:**")
            st.dataframe(df.head(max_rows))

            # 5. Check for long strings
            st.write("**Max string length per column:**")
            max_lengths = {}
            for col in df.select_dtypes(include="object").columns:
                max_lengths[col] = df[col].apply(lambda x: len(str(x)) if pd.notna(x) else 0).max()
            st.write(max_lengths if max_lengths else "No string columns")

            # 6. MultiIndex warning
            if isinstance(df.index, pd.MultiIndex):
                st.warning("DataFrame has a MultiIndex; Streamlit may flatten it. Consider formatting it for display.")

        st.markdown("<h4 style='text-align: center;'>Donors by State</h4>", unsafe_allow_html=True)
        states = stats_by_state(data)

        debug_dataframe(states)

        st.table(states)
        st.dataframe(states)

        st.space(size="small")

        st.markdown("<h4 style='text-align: center;'>Donors by City</h4>", unsafe_allow_html=True)
        cities = stats_by_city(data)
        st.dataframe(cities)

    elif page == "Donors by Time":
        st.markdown("<h2 style='text-align: center;'>Donors by Month and Year</h2>", unsafe_allow_html=True)
        st.space(size="medium")

        st.markdown("<h4 style='text-align: center;'>Donors by Year</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Years and the number of donors whose last donation was in that year.</p>", unsafe_allow_html=True)
        yearly = stats_by_year(data)
        st.bar_chart(yearly)

        st.space(size="small")
        st.markdown("<h4 style='text-align: center;'>Donors by Month</h4>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center;'>Months and the number of donors whose last donation was in that month.</p>", unsafe_allow_html=True)
        monthly = stats_by_month(data)
        st.bar_chart(monthly, sort=False)
