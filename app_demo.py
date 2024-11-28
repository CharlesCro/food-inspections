# Imports
import string
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from code.plotting.st_plots import st_plots

# Style Customization
plt.rcParams['font.family'] = 'DejaVu Sans'
st.set_page_config(layout = 'wide', page_title = 'FiFo Demo')

# load database
inspections = pd.read_csv('data/processed_chicago.csv')

def remove_punctuation(text):
    '''
        Helper function to remove punctuation from user input
    '''
    if isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    return text

def get_restaurant_data(selected_location, search_term):
    selected_data = inspections[
            (inspections["name_cleaned"].str.contains(search_term, case=False, na=False)) &
            (inspections["address"] == selected_location)
            ].sort_values(by = 'inspection_date')

    return selected_data


# Title
st.title(':blue[Fi]:red[Fo]')

# --- Sidebar Section ---
st.sidebar.title("About")
st.sidebar.divider()
st.sidebar.info(
    """
    This app allows users to search for restaurants, select a location, 
    and view graphs based on food safety data related to the selected restaurant.
    """
)


# Page Layout
left_col, mid_col, right_col = st.columns([2, 5, 2])


with left_col:
    search_term = st.text_input("Search for a restaurant:")

    # Process the user input
    search_term_cleaned = remove_punctuation(search_term)
    if search_term_cleaned:
        filtered_inspections = inspections[inspections['name_cleaned'].str.contains(search_term_cleaned, case=False, na=False)]
        if not filtered_inspections.empty:
            options = filtered_inspections["address"].unique().tolist()
            selected_location = st.selectbox("Select a location:", options)
        else:
            st.warning("No matching restaurants found. Try another search term.")
            selected_location = None
    else:
        selected_location = None

    if selected_location:
        st.divider()
        selected_data = get_restaurant_data(selected_location, search_term_cleaned)

        # Checking latest risk assessment of restaurant
        if selected_data['risk'].iloc[0] == 'Risk 1 (High)':
            st.write('Heads up! This is a :red[High] :red[Risk] establishment, which means they will receive inspections much more frequently due to their bad track record.')
        elif selected_data['risk'].iloc[0] == 'Risk 2 (Medium)':
            st.write('This is a :orange[Medium] :orange[Risk] establishment, which means they will receive inspections slightly more frequently due to their track record.')
        elif selected_data['risk'].iloc[0] == 'Risk 3 (Low)':
            st.write('This is a :green[Low] :green[Risk]establishment, which means they have performed well and \
                        not warranted extra attention from the health deparment for any critical safety violations.')
        
with mid_col:
    
    # 3. Filter dataframe and plot graphs
    if selected_location:
        st.header('History of Inspections', divider = 'red')
        # Filter dataframe based on user selection
        selected_data = get_restaurant_data(selected_location, search_term_cleaned)

        # First plot
        st_plots.plot_inspection_history(selected_data)

        with st.expander("Additional Info"):
            st.markdown("### TBD")
            
with right_col:

    if selected_location: 
        st.header('Info', divider = 'red')
        st.write('This graph helps visualize the violations broken per inspection date.')
        st.markdown('#')
        st.write('Severity of the violations are represented on scale of :blue[1] to :red[10].')
        st.write('The size of each point grows relative to the number of violations.')
        

    




















