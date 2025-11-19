import streamlit as st

st.set_page_config(
    page_title="Donor Analytics",
    page_icon="📊",
)

def run():
    st.markdown("<h1 style='text-align: center;'>Donor Analytics</h1>", unsafe_allow_html=True)

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
        # line charts, seasonality
