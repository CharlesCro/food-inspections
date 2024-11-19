# Imports
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# load database
chicago = pd.read_csv('../data/processed_chicago.csv')

# example plot function
def plot_history(data, name, address):
    '''
        This is a test function to display the violation count history of a single location
    '''
    plt.figure(figsize = (14, 4))
    
    sns.scatterplot(data = data,
                   x = data.index,
                   y = 'violation_count',
                   hue = 'inspection_type',
                   palette = 'tab10',
                   s = 200)
    
    plt.title(f'Violation Count of {name} at {address}', size = 25)
    plt.xlabel('Date of Inspection', size = 25)
    plt.ylabel('Number of Violations', size = 20)
    plt.xticks(rotation = 30)
    plt.grid(True)
    
    plt.legend(title = 'Type of Inspection', bbox_to_anchor = (1, 1))
    st.pyplot(plt.gcf())


# Streamlit code
st.title('Restaurant Inspection History')

# Search bar
restaurant_name = st.text_input('Search for a restaurant:', '')

# Filter DataFrame by restaurant name (case-insensitive)
filtered_by_name = chicago[chicago['aka_name'].str.contains(restaurant_name, case=False, na=False)]

if not filtered_by_name.empty:
    # Dropdown to pick a location
    location = st.selectbox("Choose a location:", filtered_by_name["address"].unique())

    # Filter DataFrame by location and license number
    single_restaurant = filtered_by_name[filtered_by_name["address"] == location]

    # Display the plot
    if not single_restaurant.empty:
        st.subheader(f"Data for {restaurant_name} at {location}")
        plot_history(single_restaurant, restaurant_name, location)
else:
    st.write("No matching restaurant found.")

















