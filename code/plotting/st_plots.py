'''
    This class is meant to be imported in app_demo.py and holds all plotting functions for the Streamlit app
    in order for the main app's source code to remain clean and concise. As more visualisations get developed,
    their code will be placed in this file so the Streamlit app can utilise them with ease.
'''

# Imports
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class st_plots:

    def plot_inspection_history(restaurant):
        '''
            Plots the inspection history for a restaurant, showing the severity levels of violations over time.
        '''
        # Transform violation codes and severity levels into a summarized DataFrame grouped by inspection date and severity.
        expanded_data = []
        for idx, row in restaurant.iterrows():
            for code, severity in zip(row['violation_codes'], row['severity_levels']):
                expanded_data.append([row['inspection_date'], severity])
        
        expanded_df = pd.DataFrame(expanded_data, columns=['inspection_date', 'severity_level'])
        count_df = expanded_df.groupby(['inspection_date', 'severity_level']).size().reset_index(name = 'count')
        count_df['severity_level'] = pd.to_numeric(count_df['severity_level'], errors = 'coerce')
    

        plt.figure(figsize = (10, 6))
    
        # Scatter plot of violations by severity level and inspection date.
        sns.scatterplot(data=count_df, x = 'inspection_date', y = 'severity_level', size = 'count', 
                        hue = 'severity_level', palette = 'coolwarm', sizes = (200, 1200), legend = None)
        
        # Customization.
        plt.ylim(-1, 11)
        
        plt.title('Severity Level of Violations', fontsize = 18, fontweight = 'heavy', color = 'white', pad = 20)
        plt.xlabel('Inspection Date', fontsize = 20, fontweight = 'normal', color = 'white', labelpad = 20)
        plt.ylabel('Minimal Risk                              Critical Risk', fontsize = 12, fontweight = 'bold', color = 'white')
        
        plt.xticks(fontweight = 'bold', fontsize = 10, color = 'white', rotation = 45)
        plt.yticks(fontsize = 12, fontweight = 'bold', color = 'white')
        
        plt.grid(True, linestyle = '--', alpha = 0.6, color = 'white')

        ax = plt.gca()
        
        # Set background to transparent.
        ax.set_facecolor('none')  
        plt.gcf().patch.set_facecolor('none')  
    
        # Remove borders.
        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(False)
        
        plt.tight_layout()

        # Display the plot in Streamlit.
        st.pyplot(plt)
        
        
    






























    
        