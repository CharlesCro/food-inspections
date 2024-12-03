'''
    This class is meant to be imported in app_demo.py and holds all the code for visualizations in the Streamlit app
    in order for the main app's source code to remain clean and concise. As more visualisations get developed,
    their code will be placed in this file so the Streamlit app can utilise them with ease.
'''

# Imports
import pickle
import ast
import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Override default font
plt.rcParams['font.family'] = 'DejaVu Sans'

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
                        hue = 'severity_level', palette = 'bwr', sizes = (200, 1200), legend = None)
        
        # Customization.
        plt.ylim(-1, 11)
        
        plt.title('Violation Severity Over Time', fontsize = 28, fontweight = 'bold', color = 'white', pad = 20)
        plt.xlabel('Inspection Date', fontsize = 25, fontweight = 'bold', color = 'white', labelpad = 20)
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
        
        
    def show_metrics(restaurant, chicago):
        '''
            This function will take the selected restaurant and entire database as arguments
            in order to calculate inspection data compared to other locations in the Chicago area.
        '''
        # Calculate averages of restaurant.
        avg_violations = restaurant['violation_count'].mean()
        avg_severity = restaurant['average_severity'].mean()
        success_rate = len(restaurant[restaurant['results'] == 'Pass']) / len(restaurant['results'])

        # Calculate averages of other locations.
        all_locations = chicago[chicago['name_cleaned'] == restaurant['name_cleaned'].iloc[0]]
        avg_violations_franchise = all_locations['violation_count'].mean()
        avg_severity_franchise = all_locations['average_severity'].mean()
        success_rate_franchise = len(all_locations[all_locations['results'] == 'Pass']) / len(all_locations['results'])

        # Show inspection success rate.
        value = round(success_rate * 100, 1)
        delta = round(((success_rate - success_rate_franchise) / success_rate_franchise) * 100, 1)
        if delta > 0:
            note = 'Better Than Average'
        elif delta < 0:
            note = 'Needs Improvement'
        else:
            note = 'On Par With Other Locations!'
        st.metric(label = 'Inspection Success Rate',
                value = f'{value}%',
                delta = f'{delta}% | {note}')

        # Show number of violations metric compared to other locations.
        value = round(avg_violations, 1)
        delta = round(((avg_violations - avg_violations_franchise) / avg_violations_franchise) * 100, 1)
        if delta < 0:
            note = 'Better Than Average'
        elif delta > 0:
            note = 'Needs Improvement'
        else:
            note = 'On Par With Other Locations!'
        st.metric(label = 'Average Number of Violations',
                value = f'{value}',
                delta = f'{delta}% | {note}',
                delta_color = 'inverse')
        
        # Show average severity of violations.
        value = round(avg_severity, 1)
        delta = round(((avg_severity - avg_severity_franchise) / avg_severity_franchise) * 100, 1)
        if delta < 0:
            note = 'Better Than Average'
        elif delta > 0:
            note = 'Needs Improvement'
        else:
            note = 'On Par With Other Locations!'
        st.metric(label = 'Average Severity of Violations',
                value = f'{value}',
                delta = f'{delta}% | {note}',
                delta_color = 'inverse')
        

    def get_predictions(restaurant, chicago, insp_predictor):
        '''
            This function will used the model pickled in from app_demo.py to make predictions for each inspection of a restaurant.
            Preprocessing code and decision threshold were transferred over from 02_modelling notebook.
        '''
        # This first section will generate predictions using the model passed through.
        decision_threshold = 0.2338

        restaurant['results'] = restaurant['results'].map({'Pass': 0, 'Fail': 1})
        restaurant['violation_codes'] = restaurant['violation_codes'].apply(ast.literal_eval)

        unique_codes = sorted(set(code for codes in chicago['violation_codes'].apply(ast.literal_eval) for code in codes))
        for code in unique_codes:
            column_name = f'violation_code_{code}'
            restaurant[column_name] = restaurant['violation_codes'].apply(lambda x: 1 if code in x else 0)

        risk_mapping = {'Risk 1 (High)': 3, 'Risk 2 (Medium)': 2, 'Risk 3 (Low)': 1}
        restaurant['risk'] = restaurant['risk'].map(risk_mapping)

        X = restaurant.drop(columns = ['inspection_id', 'dba_name', 'aka_name', 'license', 'facility_type', 'address', 'inspection_date', 'results',
            'violations', 'name_cleaned', 'violation_codes', 'severity_levels'])

        y_probs = insp_predictor.predict_proba(X)[:, 1]
        y_preds = pd.Series((y_probs >= decision_threshold).astype(int))


        # Assigning variables for plot.
        index = restaurant['inspection_date']
        true_labels = restaurant['results'].values
        predicted_labels = y_preds.values
        correct = (true_labels == predicted_labels).astype(int)

        # Visualising model predictions by inpsection date.
        plt.figure(figsize = (6, 6))
        plt.barh(index, correct, color = 'dodgerblue', label = 'Correct Prediction', height = 0.65)
        plt.barh(index, [1 - c for c in correct], left = correct, color = 'crimson', label = 'Incorrect Prediction', height = 0.65)

        # Annotating the bars with true vs predicted label.
        for i, (c, inc) in enumerate(zip(correct, [1 - c for c in correct])):
            label = 'Fail' if true_labels[i] else 'Pass'
            pred = 'Fail' if predicted_labels[i] else 'Pass'
            left_annot = f'Result: {label}'
            right_annot = f'Prediction: {pred}'
            # Correct prediction annotation.
            if c == 1:
                plt.text(0.05, i, left_annot, ha = 'left', va = 'center', color = 'white', fontsize = 15, fontweight = 'bold')
                plt.text(correct[i] - 0.05, i, right_annot, ha = 'right', va = 'center', color = 'white', fontsize = 15, fontweight = 'bold')
            # Incorrect prediction annotation.
            elif inc == 1:
                plt.text(correct[i] + 0.05, i, left_annot, ha = 'left', va = 'center', color = 'white', fontsize = 15, fontweight='bold')
                plt.text(inc - 0.05, i, right_annot, ha = 'right', va = 'center', color = 'white', fontsize = 15, fontweight = 'bold')

        # Further Customization.
        ax = plt.gca()
 
        ax.patch.set_alpha(0)  
        plt.gcf().patch.set_alpha(0)  

        for spine in ['top', 'right', 'left', 'bottom']:
            ax.spines[spine].set_visible(False)
        
        plt.yticks(size = 14, color = 'white')
        plt.xticks([], [])

        plt.title('Case by Case Basis', fontsize = 30, color = 'white', fontweight = 'bold', pad = 30)
        plt.legend(loc = 'lower left', fontsize = 14, labelcolor = 'white', frameon = False, bbox_to_anchor = (1, 0.5))

        # Show plot in Streamlit.
        st.pyplot(plt)

        
































    
        