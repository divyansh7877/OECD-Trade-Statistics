import matplotlib.cm

COLOR_DIC = {'Oceania': '#0000FF',
            'Europe': '#A020F0' ,
            'North America': '#028900',
            'Asia': '#ee4035',
            'South America': '#e86af0',
            'Unknown': '#d6ccc2',
            'Africa': '#ffbf00'}

def country_to_continent(country_name):
    try:
        country_alpha2 = pc.country_name_to_country_alpha2(country_name)
        country_continent_code = pc.country_alpha2_to_continent_code(country_alpha2)
        country_continent_name = pc.convert_continent_code_to_continent_name(country_continent_code)
    except:
        country_continent_name = 'Unknown'
    return country_continent_name

def continent_color(country):
    '''
    References:
     - https://www.sensationstation.net/uploads/1/1/2/2/112256989/color_by_continent.pdf
     - https://www.designpieces.com/palette/continental-ag-color-palette-hex-and-rgb/
    
    '''
    continent = country_to_continent(country)
    return COLOR_DIC[continent]

def color_map(z):
    normalize=matplotlib.colors.Normalize(vmin=min(z),vmax=max(z))  
    color_pallete_2=['#8ecae6','#219ebc','#023047','#ffb703','#fb8500']  
    newcolormap=matplotlib.colors.LinearSegmentedColormap.from_list('edge_colormap',color_pallete_2) 
    mapper=matplotlib.cm.ScalarMappable(normalize,newcolormap)  
    colors=mapper.to_rgba(z)
    return colors