import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px

filepath=r'Datasets for IV\modified_trade_data.csv'
df=pd.read_csv(filepath)
grouped = df.groupby(df.Frequency)
df_annual = grouped.get_group("Annual")
df_quarter = grouped.get_group("Quarterly")

flow = st.radio('Please choose the flow type:',["Exports", "Imports"],captions=['Trade sent by Reporter Country to Partner Country.', 'Trade recieved by Reporter Country from Partner Country.'])
freq= st.radio('Please choose the frequency type:',["Annual", "Quarterly"],captions=['Annual', 'Quarter'])
if freq == 'Annual':
    df_plot = df_annual[df_annual['Flow']==flow]
if freq == 'Quarterly':
    df_plot = df_quarter[df_quarter['Flow']==flow]

fig = px.scatter_geo(df_plot,
                     locations="LOCATION",
                     color='Reporter Continent',
                     hover_name="Reporter country",
                     size="Value",
                     animation_frame="Time",
                     projection="natural earth",
                     template = 'plotly_dark')

st.plotly_chart(fig,theme = 'streamlit')