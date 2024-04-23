import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


df=pd.read_csv(r'C:\Users\Divya\Downloads\Info Viz Project\Datasets for IV\modified_trade_data.csv')
grouped = df.groupby(df.Frequency)
df_annual = grouped.get_group("Annual")


flow = st.radio('Please choose the flow type:',["Exports", "Imports"],captions=['Trade sent by Reporter Country to Partner Country.', 'Trade recieved by Reporter Country from Partner Country.'])


time = st.select_slider('Select a color of the rainbow',options=list(df_annual['Time'].unique()))


temp=df_annual[(df_annual['Flow']==flow) & (df_annual['Time']==time)].groupby('Reporter Continent')

st.write(f'Sum of {flow} from each Continent in {time}(in USD)')
st.write(temp['Value'].sum())

#plt.figure(figsize=(16,16),dpi=400)