import streamlit as st
import pandas as pd
import random
from datetime import datetime

# Define the events and possible values
events = ['Basal Rate', 'Blood Glucose', 'Bolus', 'Carbohydrates', 'Low Battery']
values = ['1.0 Units/Hour', '120 mg/dL', '4 Units', '30 Grams']

# Generate 1000 rows of entries
timestamps = pd.date_range(start='2023-09-01', periods=1000, freq='15min')
entries = []

for timestamp in timestamps:
    if random.random() < 0.9:
        event = 'Blood Glucose'
    elif random.random() < 0.05:
        event = 'Bolus'
    else:
        event = random.choice(events)
    
    value = random.choice(values)
    value_parts = value.split(' ')
    current_value = float(value_parts[0])
    new_value = random.uniform(current_value - 5, current_value + 5)
    new_value = round(new_value, 2)
    entry = {'Timestamp': timestamp, 'Event': event, 'Value': new_value, 'Units': value_parts[1]}
    entries.append(entry)

df = pd.DataFrame(entries)

# Create the app
st.title("Insulin Pump Log Entries")

# Add 'All' option to the events list
all_events = ['All'] + events

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
st.write(filtered_df)
