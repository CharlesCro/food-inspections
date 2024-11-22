# Imports
import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt
import string
from code.plotting.st_plots import st_plots

# Style Customization
plt.rcParams['font.family'] = 'DejaVu Sans'

# load database
df = pd.read_csv('./data/processed_chicago.csv')

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

    TO DO:
    - success rate graph (finally a nice pie chart)

    - re-inspection stats (bar chart comparing first to second visit, and another violations list, also need to show if they passed after reinspection or not)

    - Summary Graphs of Other Locations of that restaurant to compare ("Maybe go to this McDonald's instead!") sort of idea.

    - Find way for common disliked violations to pop out
    examples (rodents, cross contamination, dirty bathrooms, dirty food handling, emphasis on things which a customer would want to know without getting too gross)

    - Draft app description/'help' page for how to use and interpret app

    - a hue for the text depending on risk level of restaurant

    - show inspection types in x ticks of inspection history graph

    - a specific graph for how the restaurant LAST performed.

    - Have inspection type in the xtick underneath date?
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




# # Search bar
# restaurant_name = st.text_input('Search for a restaurant:', '')

# # Filter DataFrame by restaurant name (case-insensitive)
# filtered_by_name = chicago[chicago['aka_name'].str.contains(restaurant_name, case=False, na=False)]

# if not filtered_by_name.empty:
#     # Dropdown to pick a location
#     location = st.selectbox("Choose a location:", filtered_by_name["address"].unique())

#     # Filter DataFrame by location and license number
#     single_restaurant = filtered_by_name[filtered_by_name["address"] == location]

#     # Display the plot
#     if not single_restaurant.empty:
#         st.header('Altair Plot Test')
#         st_plots.test_plot_altair(single_restaurant)
#         st.header('Seaborn Plot Test')
#         st_plots.plot_inspection_history(single_restaurant)

# else:
#     st.write("No matching restaurant found.")

















