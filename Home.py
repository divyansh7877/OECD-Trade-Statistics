import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import altair as alt
import pycountry_convert as pc
import matplotlib.cm
import numpy as np

st.write('Hello World')

filepath='Datasets for IV/modified_trade_data.csv'
df=pd.read_csv(filepath)

def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        country_continent_name = 'Unknown'
    return country_continent_name

def color_map(z):
    normalize=matplotlib.colors.Normalize(vmin=min(z),vmax=max(z))  
    color_pallete_2=['#8ecae6','#219ebc','#023047','#ffb703','#fb8500']  
    newcolormap=matplotlib.colors.LinearSegmentedColormap.from_list('edge_colormap',color_pallete_2) 
    mapper=matplotlib.cm.ScalarMappable(normalize,newcolormap)  
    colors=mapper.to_rgba(z)
    return colors

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

G = nx.from_pandas_edgelist(df_plot,
                            source='Reporter country',
                            target='Partner country',
                            edge_attr='Value',
                            create_using=nx.DiGraph)


COLOR_DIC = {'Oceania': '#0000FF',
            'Europe': '#A020F0' ,
            'North America': '#028900',
            'Asia': '#ee4035',
            'South America': '#e86af0',
            'Unknown': '#d6ccc2',
            'Africa': '#ffbf00'}

def continent_color(country):
    '''
    References:
     - https://www.sensationstation.net/uploads/1/1/2/2/112256989/color_by_continent.pdf
     - https://www.designpieces.com/palette/continental-ag-color-palette-hex-and-rgb/
    
    '''
    continent = country_to_continent(country)
    return COLOR_DIC[continent]



options = {
    'with_labels':False,
    'node_color': [continent_color(country) for country in list(G.nodes)] ,# color of node
    'node_size': 800,          # size of node
    'width': 1,                 # line width of edges
    'arrowsize': 18,            # size of arrow
    'edge_color':color_map(df_plot['Value']),        # edge color
    'label': ['Oceania', 'Europe', 'North America', 'Asia', 'South America','Unknown', 'Africa']
}
fig = plt.figure(figsize=(16,16),dpi=400)
nx.draw_networkx(G, pos=nx.circular_layout(G),**options)

option_node_labels={'horizontalalignment' :'left',
                    'verticalalignment' :'center_baseline',
                    'clip_on':True
                    }

nx.draw_networkx_labels(G,pos=nx.circular_layout(G),**option_node_labels)

# plt.savefig('testimg.pdf',format='pdf')

st.pyplot(fig)