import streamlit as st
import pandas as pd
import plost

# Setting up the page configuration
st.set_page_config(page_title="Kwh and Outdoor Temp Dashboard", layout="wide", initial_sidebar_state="expanded")
st.write("# My first kwh dashboard in python :) ")

# Applying custom styles
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Loading temperature data
df_temp = pd.read_csv("out_temp.csv", header=0) 

# Combine Date and Time into a single datetime column with proper parsing
df_temp['Datetime'] = pd.to_datetime(df_temp['Date'] + ' ' + df_temp['Time'], format='%d-%m-%Y %H:%M')
df_temp.set_index('Datetime', inplace=True)

# Loading kwh data
df_kwh = pd.read_csv("kwh.csv", header=0)
df_kwh['Date'] = pd.to_datetime(df_kwh['Date'], format='%d-%m-%Y')
df_kwh.set_index('Date', inplace=True)

# Sidebar configuration
st.sidebar.header("My Dashboard")
st.sidebar.subheader('Heat map parameter')
time_hist_color = st.sidebar.selectbox('Color by', ('Temperature',)) 

st.sidebar.subheader('Line chart parameters')
plot_data = st.sidebar.multiselect('Select data', ['Temperature'], ['Temperature'])
plot_height = st.sidebar.slider('Specify plot height', 200, 500, 250)

st.sidebar.markdown("Created by Kim Rosvoll")

# Display metrics
st.markdown('### Metrics')
col1, col2 = st.columns(2)
col1.metric("Temperature", f"{df_temp['Temperature'].mean():.1f} °C", f"{df_temp['Temperature'].diff().mean():.1f} °C")
col2.metric("Kwh Now", f"{df_kwh['Kwh'].iloc[-1]}")

# Plotting the heatmap
st.markdown('### Heatmap')
plost.time_hist(
    data=df_temp,
    date='Datetime',
    x_unit='day',
    y_unit='hour',
    color=time_hist_color,
    aggregate='mean',
    legend=None
)

# Plotting the line chart for temperature data
st.markdown('### Temperature Line Chart')
st.line_chart(df_temp[plot_data], height=plot_height)

# Plotting the line chart for kwh data
st.markdown('### Kwh Line Chart')
st.line_chart(df_kwh['Kwh'], height=plot_height)
