
'''
FiFo Demo Streamlit App

This app enables users to explore food safety inspection data for restaurants in Chicago. 
Features include:
- A search bar to find restaurants by name.
- A dropdown to select restaurant locations.
- Visualisations of inspection history.
- Sidebars with app information and instructions.

The app provides insights into food safety violations and risk assessments, 
helping users make informed decisions before deciding where to eat.
'''

# Imports
import string
import pickle
import ast

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from code.plotting.st_plots import st_plots

# Style customization.
plt.rcParams['font.family'] = 'DejaVu Sans'
st.set_page_config(layout = 'wide', page_title = 'FiFo Demo')

# Load database.
inspections = pd.read_csv('data/processed_chicago.csv')

# Load model.
with open('models/predict_inspection.pkl', 'rb') as pickle_in:
    insp_predictor = pickle.load(pickle_in)

def remove_punctuation(text):
    '''
        Helper function to remove punctuation from user input.
    '''
    if isinstance(text, str):
        return text.translate(str.maketrans('', '', string.punctuation))
    return text

def get_restaurant_data(selected_location, search_term):
    '''
        This function will return a specific restaurant's inspection data
        given a name and address.
    '''
    selected_data = inspections[
            (inspections['name_cleaned'].str.contains(search_term, case = False, na = False)) &
            (inspections['address'] == selected_location)
            ].sort_values(by = 'inspection_date')

    return selected_data

def get_prediction(restaurant):
    '''
        This function will used the model pickled in to make predictions for each inspection of a restaurant.
        Preprocessing code and decision threshold were transferred over from 02_modelling notebook.
    '''
    decision_threshold = 0.2338

    restaurant['results'] = restaurant['results'].map({'Pass': 0, 'Fail': 1})

    restaurant['violation_codes'] = restaurant['violation_codes'].apply(ast.literal_eval)

    unique_codes = sorted(set(code for codes in inspections['violation_codes'].apply(ast.literal_eval) for code in codes))

    for code in unique_codes:
        column_name = f'violation_code_{code}'
        restaurant[column_name] = restaurant['violation_codes'].apply(lambda x: 1 if code in x else 0)

    risk_mapping = {'Risk 1 (High)': 3, 'Risk 2 (Medium)': 2, 'Risk 3 (Low)': 1}
    restaurant['risk'] = restaurant['risk'].map(risk_mapping)

    X = restaurant.drop(columns = ['inspection_id', 'dba_name', 'aka_name', 'license', 'facility_type', 'address', 'inspection_date', 'results',
       'violations', 'name_cleaned', 'violation_codes', 'severity_levels'])
    
    y_probs = insp_predictor.predict_proba(X)[:, 1]
    y_preds = (y_probs >= decision_threshold).astype(int)

    y_preds = pd.Series(y_preds).map({0: 'Pass', 1: 'Fail'})

    return y_preds



# --- Streamlit App Page ---

# Set page title.
st.title(':blue[Fi]:red[Fo]')

# Sidebar section.
st.sidebar.title('About')
st.sidebar.divider()
st.sidebar.info(
    """
    This app allows users to search for restaurants, select a location, 
    and view graphs and other important info based on food safety data related to the selected restaurant.
    """
)

# Set page layout.
left_col, mid_col, right_col = st.columns([2, 5, 2])


with left_col:
    # Create search bar.
    search_term = st.text_input('Search for a restaurant:')

    # Process the user input.
    search_term_cleaned = remove_punctuation(search_term)

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
        st.divider()
        selected_data = get_restaurant_data(selected_location, search_term_cleaned)

        # Checking latest risk assessment of restaurant.
        if selected_data['risk'].iloc[0] == 'Risk 1 (High)':
            st.write('Heads up! This is a :red[High] :red[Risk] establishment')
        elif selected_data['risk'].iloc[0] == 'Risk 2 (Medium)':
            st.write('This is a :orange[Medium] :orange[Risk] establishment')
        elif selected_data['risk'].iloc[0] == 'Risk 3 (Low)':
            st.write('This is a :green[Low] :green[Risk]establishment')

with mid_col:
    
    # Filter dataframe and plot graphs.
    if selected_location:
        st.header('History of Inspections', divider = 'red')
        # Filter dataframe based on user selection.
        selected_data = get_restaurant_data(selected_location, search_term_cleaned)

        # First plot.
        st_plots.plot_inspection_history(selected_data)

        with st.expander('Beta Test Classification Model'):
            st.header('Let\'s see how our little :blue[Fi]:red[Fo] model performs. Please be kind, he\'s still learning!', divider = 'blue')

            y_true = selected_data['results']

            y_preds = get_prediction(selected_data)

            for i in range(len(selected_data)):
                name = selected_data.iloc[i]['aka_name']
                date = selected_data.iloc[i]['inspection_date']
                true = f':blue[{y_true.iloc[i]}]' if y_true.iloc[i] == 'Pass' else f':red[{y_true.iloc[i]}]'
                pred = f':blue[{y_preds.iloc[i]}]' if y_preds.iloc[i] == 'Pass' else f':red[{y_preds.iloc[i]}]'

                st.header(f'Inspection of {date}', divider = 'red')
                st.write(f'The actual result was {true}')
                st.write(f'The model predicted {pred}')

                if true == pred:
                    st.header('Nice! Good job little :blue[Fi]:red[Fo]!')
                else:
                    st.header('Oof! Go study some more little :blue[Fi]:red[Fo]!')

                st.divider()


                

                
            
with right_col:
    # Details section explaining graphs.
    if selected_location: 
        st.header('Info', divider = 'red')
        st.write('This graph helps visualize the violations broken per inspection date.')
        st.markdown('#')
        st.write('Severity of the violations are represented on scale of :blue[1] to :red[10].')
        st.write('The size of each point grows relative to the number of violations.')
        

    




















