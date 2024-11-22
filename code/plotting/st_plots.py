import altair as alt
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

class st_plots:

    def plot_inspection_history(df):
        '''
            This is a improved test function to display the inspection history of a single location
        '''
        expanded_data = []
        for idx, row in df.iterrows():
            for code, severity in zip(row['violation_codes'], row['severity_levels']):
                expanded_data.append([row['inspection_date'], severity])
        
        expanded_df = pd.DataFrame(expanded_data, columns=['inspection_date', 'severity_level'])
        count_df = expanded_df.groupby(['inspection_date', 'severity_level']).size().reset_index(name='count')
        count_df['severity_level'] = pd.to_numeric(count_df['severity_level'], errors='coerce')
    
        plt.figure(figsize=(10, 6))
    
        # Use a simple, modern color palette that fits with Streamlit's aesthetic
        sns.scatterplot(data=count_df, x='inspection_date', y='severity_level', size='count', 
                        hue='severity_level', palette='coolwarm', sizes=(200, 1200), legend=None)
        
        # Step 6: Set y-axis limits from 1 to 10
        plt.ylim(-1, 11)
        
        # Step 7: Customize the plot for dark theme and white labels/lines
        plt.title('Severity Level of Violations', fontsize=18, fontweight='heavy', color='white', pad = 20)
        plt.xlabel('Inspection Date', fontsize=20, fontweight='normal', color='white', labelpad = 20)
        plt.ylabel('Minimal Risk                              Critical Risk', fontsize=12, fontweight='bold', color='white')
        
        # Customize tick labels for readability and style (make them white)
        plt.xticks(fontweight = 'bold', fontsize=10, color='white', rotation = 45)
        plt.yticks(fontsize=12, fontweight = 'bold', color='white')
        
        # Change grid lines to white, with subtle dashed style
        plt.grid(True, linestyle='--', alpha=0.6, color='white')
        
        # Set background to transparent (for embedding in Streamlit with a dark background)
        plt.gca().set_facecolor('none')  # Transparent background for the axes
        plt.gcf().patch.set_facecolor('none')  # Transparent figure background
    
        # Remove border
        ax = plt.gca()
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        
        # Display the plot in Streamlit
        st.pyplot(plt)
        
        # Ensure layout is tight for better display
        plt.tight_layout()
    
    
    def test_plot_altair(df):
        '''
            This is a test function to display the violation count history of a single location
            Using Altair
        '''
        # to use index as X value in altair
        df = df.reset_index().rename(columns={'inspection_date': 'Date'})
        
        # Altair Plot
        # Create Altair scatter plot
        scatter_plot = alt.Chart(df).mark_circle(
            size=350,  # Size of dots
            color='crimson',  # Color of dots
            stroke='black',  # Border color
            strokeWidth=1.5,  # Border width
            opacity=0.8  # Transparency for a modern look
        ).encode(
            x=alt.X('Date', title='Inspection Date', axis=alt.Axis(labelAngle=0)),  # Use index as X-axis
            y=alt.Y('violation_count', title='Number of Violations'),  # Y-axis from the 'y' column
            tooltip=['Date', 'violation_count']  # Add tooltips for interactivity
        ).properties(
            width=600,  # Chart width
            height=400,  # Chart height
            title="Violation Count by Inspection"
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=20,
            grid=True  # Minimalistic look by removing grid lines
        ).configure_title(
            fontSize=30,
            font='Arial',
            anchor='middle',
            color='white'
        )
    
        # Render the chart in Streamlit
        st.altair_chart(scatter_plot, use_container_width=True)































    
        