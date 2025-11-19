import streamlit as st

dataset_merger = st.Page("pages/dataset_merger.py", title="Dataset Merger", icon="📁", default=True)
analytics = st.Page("pages/analytics.py", title="Donor Analytics", icon="📈")

current_page = st.navigation([dataset_merger, analytics], position="sidebar")
current_page.run()