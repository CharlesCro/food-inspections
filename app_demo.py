
'''
FiFo Demo Streamlit App

This app enables users to explore food safety inspection data for restaurants in Chicago. 
Features include:
- A search bar to find restaurants by name.
- A dropdown to select restaurant locations.
- Visualisations and metrics of inspection history.
- Functionality to see how my classification model performs on a restaurant's inspections.

The app provides insights into food safety violations and risk assessments, 
helping users make informed decisions before deciding where to eat.
'''

# Imports
import pickle

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.libs.st_helpers import Stats, Utils

# Style customization.
st.set_page_config(layout = 'wide', page_title = 'FiFo Demo')

# Load database.
inspections = pd.read_csv('data/processed_chicago.csv')

# Load model.
with open('models/predict_inspection.pkl', 'rb') as pickle_in:
    insp_predictor = pickle.load(pickle_in)


# --- Streamlit App Page ---

# Set page title.
st.title(':blue[Fi]:red[Fo]')

# Sidebar section.
st.sidebar.title('About')
st.sidebar.divider()
st.sidebar.info(
    '''
    The :blue[Fi]:red[Fo] app allows users to search for restaurants in the Chicago area, select a location, 
    and view graphs and other important info based on food safety data related to the selected restaurant.
    ---

    ---

    You may also test my classification model :blue[Jeffrey] on restaurant inspection results and see how he does.
    Please be kind to :blue[Jeffrey], he's still learning! 

    ---

    :orange[Developed] :orange[by:]
    Charles Crocicchia
    '''
)

# Set page layout.
left_col, mid_col, right_col = st.columns([2, 5, 2])


with left_col:
    # Create search bar.
    search_term = st.text_input('Search for a restaurant:')

    # Process the user input.
    search_term_cleaned = Utils.remove_punctuation(search_term)

    # Once a user input is received, check that restaurant exists in database, then provide all locations.
    if search_term_cleaned:
        filtered_inspections = inspections[inspections['name_cleaned'].str.contains(search_term_cleaned, case=False, na=False)]
        if not filtered_inspections.empty:
            options = filtered_inspections['address'].unique().tolist()
            selected_location = st.selectbox('Select a location:', options)
        else:
            st.warning("No matching restaurants found. Try another search term.")
            selected_location = None
    else:
        selected_location = None

    if selected_location:
        selected_data = Utils.get_restaurant_data(selected_location, search_term_cleaned, inspections)

        # Display comparison metrics if franchise
        if len(options) > 1:
            st.header('Versus Other Locations', divider = 'blue')

            Stats.show_comparison_metrics(selected_data, inspections)

with mid_col:
    
    # Filter dataframe and plot graphs.
    if selected_location:
        st.header('History of Inspections', divider = 'red')
        # Filter dataframe based on user selection.
        selected_data = Utils.get_restaurant_data(selected_location, search_term_cleaned, inspections)

        # Visualise inspection violations over time.
        Stats.plot_inspection_history(selected_data)

        with st.expander('Beta Test Classification Model'):
            st.header('Predictions of This Restaurant\'s Inspections', divider = 'red')

            # Visualise model predictions vs true labels.
            Stats.show_predictions(selected_data, inspections, insp_predictor)
            
with right_col:
    # Details section explaining graphs.
    if selected_location:
        selected_data = Utils.get_restaurant_data(selected_location, search_term_cleaned, inspections)

        st.header('Info', divider = 'red')
        st.markdown('''
                    - This graph helps visualize the violations broken per inspection.
                    - Severity of the violations are represented on scale of :blue[1] to :red[10].
                    - The size of each point grows relative to the number of violations.
                    - Inspections are :red[Red] if they failed or :blue[Blue] if they passed.
                    ''')

        # Checking latest risk assessment of restaurant.
        if selected_data['risk'].iloc[0] == 'Risk 1 (High)':
            st.write('This is a :red[High] :red[Risk] establishment')
        elif selected_data['risk'].iloc[0] == 'Risk 2 (Medium)':
            st.write('This is a :orange[Medium] :orange[Risk] establishment')
        elif selected_data['risk'].iloc[0] == 'Risk 3 (Low)':
            st.write('This is a :green[Low] :green[Risk]establishment')

        with st.expander('Risk Explained'):
            st.write('''
                        :red[1.] :red[High] :red[Risk]: These establishments handle complex food preparations, like cooking, cooling, reheating, or handling raw ingredients extensively. They also serve vulnerable populations or use advanced techniques like vacuum packaging.

                        :orange[2.] :orange[Medium] :orange[Risk]: These places serve foods prepared the same day or minimally assembled from pre-approved sources, with simpler processes compared to high-risk facilities.

                        :blue[3.] :blue[Low] :blue[Risk]: These serve mostly prepackaged or simple foods and drinks, with minimal preparation or handling of potentially hazardous items.
                     ''')


    




















