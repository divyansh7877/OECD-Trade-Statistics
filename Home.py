import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import altair as alt
import pycountry_convert as pc
import matplotlib.cm
import numpy as np


from funcs import country_to_continent,continent_color,color_map
from funcs import COLOR_DIC



st.title('International Trade Statistics')

st.write('Hello World')

filepath='Datasets for IV/modified_trade_data.csv'
df=pd.read_csv(filepath)


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

time = st.select_slider('Select timeline',
                        options=list(df_plot['Time'].unique()))
flow=st.radio('Please choose the flow type:',
                ["Exports", "Imports"],
                captions=['Trade sent by Reporter Country to Partner Country.', 'Trade recieved by Reporter Country from Partner Country.'])


vleft,vright = min(df_plot['Value']),max(df_plot['Value'])
v_left,v_right= st.slider('Select a range of values',vleft,vright,(vleft,vright))

df_fplot = df_plot[(df_plot['Flow']==flow) & (df_plot['Time']==time) & (df_plot['Value']>=v_left) & (df_plot['Value']<=v_right)]

G = nx.from_pandas_edgelist(df_fplot,
                            source='Reporter country',
                            target='Partner country',
                            edge_attr='Value',
                            create_using=nx.DiGraph)

cmap_edge,mapper= color_map(df_fplot['Value'])
options = {
    'with_labels':False,
    'node_color': [continent_color(country) for country in list(G.nodes)] ,# color of node
    'node_size': 800,          # size of node
    'width': 1,                 # line width of edges
    'arrowsize': 18,            # size of arrow
    'edge_color':cmap_edge,        # edge color
    'label': ['Oceania', 'Europe', 'North America', 'Asia', 'South America','Unknown', 'Africa']
}


fig = plt.figure(figsize=(15,12),dpi=400)
nx.draw_networkx(G, pos=nx.circular_layout(G),**options)

option_node_labels={'horizontalalignment' :'left',
                    'verticalalignment' :'center_baseline',
                    'clip_on':True
                    }

nx.draw_networkx_labels(G,pos=nx.circular_layout(G),**option_node_labels)
plt.colorbar(mapper,shrink =0.5)
st.pyplot(fig)

