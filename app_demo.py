# Imports
import string
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from code.plotting.st_plots import st_plots

# Style Customization
plt.rcParams['font.family'] = 'DejaVu Sans'

# load database
df = pd.read_csv('data/processed_chicago.csv')

def remove_punctuation(text):
    '''
        Helper function to remove punctuation from user input
    '''
    if isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    return text


# --- Sidebar Section ---
st.sidebar.title("About")
st.sidebar.divider()
st.sidebar.info(
    """
    This app allows users to search for restaurants, select a location, 
    and view graphs based on food safety data related to the selected restaurant.
    """
)

# --- Main App Section ---
st.title(':blue[Fi]:red[Fo] Demo', anchor = False)
st.divider()

# Layout: Create two columns for search and dropdown
col1, col2 = st.columns([1, 1])

# 1. Search Bar
with col1:
    search_term = st.text_input("Search for a restaurant:")

# Process the user input
search_term_cleaned = remove_punctuation(search_term)

# 2. Display matching restaurant names and locations for selection
with col2:
    if search_term:
        filtered_df = df[df["aka_name"].str.contains(search_term, case=False, na=False)]
        if not filtered_df.empty:
            options = filtered_df["address"].unique().tolist()
            selected_location = st.selectbox("Select a location:", options)
        else:
            st.warning("No matching restaurants found. Try another search term.")
            selected_location = None
    else:
        selected_location = None



# 3. Filter dataframe and plot graphs
if selected_location:
    # Filter dataframe based on user selection
    selected_data = df[
        (df["aka_name"].str.contains(search_term, case=False, na=False)) &
        (df["address"] == selected_location)
    ].sort_values(by = 'inspection_date')
    
    st.divider()
    st.markdown('''
                ## Inspection History
                - Dots scaling with number of violations
                - **Danger Zone:** 7 or higher severity level
                ''')
    st_plots.plot_inspection_history(selected_data)
    
st.markdown("---")


















