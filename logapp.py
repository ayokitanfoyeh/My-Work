import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Define the events and possible values
events_values = {
    'Insulin Basal Rate': {'unit': 'Units/Hour', 'min': 0.5, 'max': 2.0},
    'Blood Glucose Level': {'unit': 'mg/dL', 'min': 70, 'max': 180},
    'Insulin Bolus Dose': {'unit': 'Units', 'min': 1, 'max': 10},
    'Battery Level': {'unit': '%', 'min': 0, 'max': 100}
}

# Generate 1000 rows of entries
timestamps = pd.date_range(start='2023-09-01', periods=1000, freq='15min')
entries = []

for timestamp in timestamps:
    if random.random() < 0.9:
        event = 'Blood Glucose Level'
    elif random.random() < 0.05:
        event = 'Insulin Bolus Dose'
    else:
        event = random.choice(list(events_values.keys()))
    
    unit = events_values[event]['unit']
    
    if event == 'Battery Level':
        new_value = 10
    else:
        min_value = events_values[event]['min']
        max_value = events_values[event]['max']
        new_value = random.uniform(min_value, max_value)
    
    new_value = round(new_value, 2)
    
    entry = {'Timestamp': timestamp, 'Event': event, 'Value': new_value, 'Units': unit}
    entries.append(entry)

df = pd.DataFrame(entries)

# Set the index name to "Log ID"
df.index.name = "Log ID"

# Create the app
st.title("Insulin Pump Log Entries")

# Add radio button for Log ID filter
log_id_filter = st.radio("Filter by Log ID:", ('All Logs', 'Specific Log ID'))

# If 'Specific Log ID' is selected, show number input for Log ID
if log_id_filter == 'Specific Log ID':
    specific_log_id = st.number_input("Enter Log ID", min_value=0, max_value=len(df) - 1, value=0)
    filtered_df_by_id = df[df.index == specific_log_id]
    
    if filtered_df_by_id.empty:
        st.write("No entries found for the specified Log ID.")
    else:
        st.write("Log Entries:")
        st.dataframe(filtered_df_by_id)
else:
    # Add 'All' option to the events list
    all_events = ['All'] + list(events_values.keys())

    # Filter by event
    selected_event = st.selectbox("Filter by Event", all_events)

    if selected_event == 'All':
        filtered_df = df.copy()
    else:
        filtered_df = df[df['Event'] == selected_event]

    # Get the earliest and latest dates from the DataFrame
    earliest_date = df['Timestamp'].min().date()
    latest_date = df['Timestamp'].max().date()

    # Filter by date
    start_date = st.date_input("Filter by Start Date", value=earliest_date)
    end_date = st.date_input("Filter by End Date", value=latest_date)

    start_date = pd.Timestamp(datetime.combine(start_date, datetime.min.time()))
    end_date = pd.Timestamp(datetime.combine(end_date, datetime.max.time()))

    filtered_df = filtered_df[(filtered_df['Timestamp'] >= start_date) & (filtered_df['Timestamp'] <= end_date)]

    # Display the filtered DataFrame
    st.write("Log Entries:")
    st.dataframe(filtered_df)
