import altair as alt
import streamlit as st
import pandas as pd

st.header('Matrix Based Analysis')

df=pd.read_csv('Datasets for IV/modified_trade_data.csv')
grouped = df.groupby(df.Frequency)
df_annual = grouped.get_group("Annual")
df_quarter = grouped.get_group("Quarterly")

freq = st.radio('Please select Freqency.',
                ['Annual','Quarter'],
                )

if freq=='Annual':
    df_plot=df_annual
elif freq=='Quarter':
    df_plot=df_quarter

flow = st.radio('Please choose the flow type:',
                ["Exports", "Imports"],
                captions=['Trade sent by Reporter Country to Partner Country.', 'Trade recieved by Reporter Country from Partner Country.'])

time = st.select_slider('Select timeline',
                        options=list(df_plot['Time'].unique()))

source = df_plot[(df_plot['Flow']==flow) & (df_plot['Time']==time)]
chart=alt.Chart(source).mark_rect().encode(
    x='Partner country:N',
    y='Reporter country:N',
    color=alt.Color('Value:Q',scale=alt.Scale(scheme='sinebow')),
    tooltip = ['Value','Flow']
)
st.altair_chart(chart, theme="streamlit")