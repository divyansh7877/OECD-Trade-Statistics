import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt


st.header('Continental Analysis')

df=pd.read_csv('Datasets for IV/modified_trade_data.csv')
grouped = df.groupby(df.Frequency)
df_annual = grouped.get_group("Annual")
df_quarter = grouped.get_group("Quarterly")

freq = st.radio('Please select Freqency.',
                ['Annual','Quarter'],
                )

# flow = st.radio('Please choose the flow type:',
#                 ["Exports", "Imports"],
#                 captions=['Trade sent by Reporter Country to Partner Country.', 'Trade recieved by Reporter Country from Partner Country.'])

if freq=='Annual':
    df_plot=df_annual
elif freq=='Quarter':
    df_plot=df_quarter

time = st.select_slider('Select timeline',
                        options=list(df_plot['Time'].unique()))

continental = pd.DataFrame(columns = ['Exports','Imports'])
continental['Exports']=df_plot[(df_plot['Flow']=='Exports') & (df_plot['Time']==time)].groupby('Reporter Continent')['Value'].sum()
continental['Imports']=df_plot[(df_plot['Flow']=='Imports') & (df_plot['Time']==time)].groupby('Reporter Continent')['Value'].sum()

st.write(f'Sum from each Continent in {time}(in USD)')
st.dataframe(continental)
