import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd
import contextily as cx
from shapely import wkt
import networkx as nx
from pyvis.network import Network
import altair as alt
import nx_altair as nxa
import pycountry_convert as pc
import matplotlib.cm
import numpy as np

st.write('Hello World')

filepath=r'Datasets for IV\60dde6d7-en\QITS-2023-1-EN-20240216T090213.csv'
df=pd.read_csv(filepath)
df=df.drop(columns=['Unit Code', 'Unit', 'PowerCode Code', 'PowerCode',
       'Reference Period Code', 'Reference Period', 'Flag Codes','Flags'])

df.replace('Korea','South Korea',inplace=True)

def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        country_continent_name = 'Unknown'
    return country_continent_name

def color_map(z):

    colors = np.zeros((np.size(z),3))  # Not needed.
    
    normalize=matplotlib.colors.Normalize(vmin=min(z),vmax=max(z))  # Normalize elevation values to float values between 0 and 1

    # Different custom color_palletes, help from coloors.co
    color_pallete_1=["#001524","#15616D","#FFECD1","#FF7D00","#FF7D00",'#78290F']  
    color_pallete_2=['#8ecae6','#219ebc','#023047','#ffb703','#fb8500']  # Best
    color_pallete_3=["#03045e","#023e8a","#0077b6","#0096c7","#00b4d8","#48cae4","#90e0ef","#ade8f4","#caf0f8"] # bad
    color_pallete_4=["#006ba6","#0496ff","#ffbc42","#d81159","#8f2d56"] # bad

    newcolormap=matplotlib.colors.LinearSegmentedColormap.from_list('edge_colormap',color_pallete_2) 
    mapper=matplotlib.cm.ScalarMappable(normalize,newcolormap)  

    colors=mapper.to_rgba(z)
    return colors


df['Reporter Continent']=df['Reporter country'].apply(country_to_continent)
df['Partner Continent']=df['Partner country'].apply(country_to_continent)


grouped = df.groupby(df.Frequency)
df_annual = grouped.get_group("Annual")
df_quarter = grouped.get_group("Quarterly")




g1=df_annual.groupby(df_annual.Time)
date=st.radio('Choose the time',list(df_annual.Time.unique()))
flow='Exports'
df_annual_t=g1.get_group(date)
df_annual_plot = df_annual_t[df_annual_t['Flow']==flow]

G = nx.from_pandas_edgelist(df_annual_plot,
                            source='Reporter country',
                            target='Partner country',
                            edge_attr='Value',
                            create_using=nx.DiGraph)


COLOR_DIC = {'Oceania': '#0000FF',
            'Europe': '#A020F0' ,
            'North America': '#028900',
            'Asia': '#ee4035',
            'South America': '#e86af0',
            'Unknown': '#000000',
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
    'edge_color':color_map(df_annual_plot['Value']),        # edge color
    'label': ['Oceania', 'Europe', 'North America', 'Asia', 'South America','Unknown', 'Africa']
}
fig = plt.figure(figsize=(16,16),dpi=400)
nx.draw_networkx(G, pos=nx.circular_layout(G),**options)

option_node_labels={'horizontalalignment' :'left',
                    'verticalalignment' :'center_baseline',
                    'clip_on':True
                    }



nx.draw_networkx_labels(G,pos=nx.circular_layout(G),**option_node_labels)

plt.savefig('testimg.pdf',format='pdf')



st.pyplot(fig)