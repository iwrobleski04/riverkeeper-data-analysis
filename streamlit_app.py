import streamlit as st

dataset_merger = st.Page("dataset_merger.py", title="Dataset Merger", icon="📁", default=True)
analytics = st.Page("analytics.py", title="Donor Analytics", icon="📊")

current_page = st.navigation([dataset_merger, analytics], position="top")
current_page.run()