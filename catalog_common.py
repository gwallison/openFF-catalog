"""catalog_common.py
Used as the first thing in all jupyter index files.
This is the first thing executed.

Passing arguments in:
sys.argv:
0 = this scripts name
1 = header title - no spaces! use '_' to indicate spaces
"""
import datetime
import sys
from IPython.display import Markdown as md
from IPython.core.display import display, HTML
#import geopandas as gpd


import warnings
warnings.filterwarnings('ignore')


#repo_name = 'v14_2022_04_06'
repo_name = 'v14_BETA_2022_06_25'
bulkdata_date = 'June 25, 2022'
cat_creation_date = datetime.datetime.now()
extData_loc = 'c:/MyDocs/OpenFF/data/external_refs/'
transformed_loc = 'c:/MyDocs/OpenFF/data/transformed/'


def ID_header(title = '',line2 ='', subtitle = '',imagelink='',
              incl_links=True,link_up_level=False):
#     if len(sys.argv)<2:
#         title = ''
#     else:
#         title = sys.argv[1].replace('_',' ')
    local_prefix = ''
    if link_up_level:
        local_prefix= '../'
        
    logo = """<img src="https://storage.googleapis.com/open-ff-common/openFF_logo.png" alt="openFF logo" width="100" height="100">"""
    source = f"""This file generated on {cat_creation_date:%B %d, %Y} from data repository: {repo_name}."""
    cat_links = f"""<td width=20%>
                    <p style="text-align: center; font-size:120%"> 
                      <a href="https://frackingchemicaldisclosure.wordpress.com/data-navigator/"> Navigator </a><br>
                      <a href="{local_prefix}Open-FF_Chemicals.html" title="OpenFF Chemical index"> Chemical Index </a><br>
                      <a href="{local_prefix}Open-FF_Synonyms.html" title="OpenFF Synonyms index"> Synonym Index </a><br>
                      <a href="{local_prefix}Open-FF_Companies.html" title="OpenFF Company names translation table"> Company Translation table </a><br>
                      <a href="https://codeocean.com/capsule/9423121/tree" title="Source code and reference data sets"> CodeOcean Project </a><br>
                    </p>
                    </td>
                """
    #                       <a href="https://frackingchemicaldisclosure.wordpress.com/"> Blog </a><br>
    #                <p style="text-align: left; font-size:120%"> Links: </p>

    if incl_links: cat_txt = cat_links
    else: cat_txt = ''
    line2_alt = ''
    if line2:
        line2_alt = f'<p style="text-align: center; font-size:250%">{line2}</p><br>'
    subtitle_alt = ''
    if subtitle:
        subtitle_alt = f'<p style="text-align: center; font-size:180%">{subtitle}</p>'
    image_alt = ''
    if imagelink:
        image_alt = f'<center>{imagelink}</center>'
        
    table = f"""<style>
                </style>
                <table style='margin: 0 auto' >
                <tr>
                <td width=10%>{logo}</td>
                <td><p style="text-align: center; font-size:300%">{title}</p><br> {line2_alt} {subtitle_alt} {image_alt}
                    <p style="text-align: center; font-size:100%">{source}
                </td>
                {cat_txt}
            </table>"""
    display(HTML(table))

###############################  Used to make repository accessible ####################
#import sys
sys.path.insert(0,'c:/MyDocs/OpenFF/src/')
import common.code.Analysis_set_remote as ana_set
import common.code.get_repo_data as grd
import common.code.get_google_map as ggmap

def set_page_param():
    # #############################  Make indices full page ###################################
    display(HTML("<style>.jp-Cell { width: 80% !important; }</style>"))


###########################  for itables #####################################
# this code is necessary to keep itables working with new ngcovert templates
#from IPython.display import HTML, display
from time import sleep
display(HTML("""
<script src="https://cdnjs.cloudflare.com/ajax/libs/require.js/2.1.10/require.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.0.3/jquery.min.js"></script>
"""))
sleep(0.1)

##################### functions for creating links and making displays a little nicer
from math import log10, floor
def round_sig(x, sig=2):
    try:
        if abs(x)>=1:
            out =  int(round(x, sig-int(floor(log10(abs(x))))-1))
            return f"{out:,d}" # does the right thing with commas
        else: # fractional numbers
            return str(round(x, sig-int(floor(log10(abs(x))))-1))
    except:
        return x
    
# used to insert links of google maps into tables
def make_clickable(val):
    try:
        if val[:4]=='http':
            return '<a href="{}" target="_blank">{}</a>'.format(val,'map')
    except:
        return val
    return val

def getLink(row):
    return ggmap.getSearchLink(row.bgLatitude,row.bgLongitude)

def getCatLink(cas,text_to_show='Analysis',use_remote=False):
    preamble = ''
    if use_remote:
        preamble = 'https://qbobioyuz1dh57rst8exeg-on.drv.tw/open_FF_catalog/'
    s = f'{preamble}{cas}/analysis_{cas}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getStateLink(state,text_to_show='State details',use_remote=False):
    preamble = 'states'
    if use_remote:
        preamble = 'https://qbobioyuz1dh57rst8exeg-on.drv.tw/open_FF_catalog/states/'
    s = f'{preamble}/{state.lower()}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getCountyLink(county,state,text_to_show='County details',use_remote=False):
    preamble = '.' # when coming from a state link, don't need preamble
    if use_remote:
        preamble = 'https://qbobioyuz1dh57rst8exeg-on.drv.tw/open_FF_catalog/states/'
    name = county.lower().replace(' ','_') + '-' + state.lower().replace(' ','_')
    s = f'{preamble}/{name}.csv'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getDataLink(cas):
    s = f'{cas}/data.zip'
    return ggmap.wrap_URL_in_html(s,'zipped data file')

def getChemIDLink(cas):
    try:
        if cas[0] in ['0','1','2','3','4','5','6','7','8','9']:
            s = f'https://chem.nlm.nih.gov/chemidplus/rn/{cas}'
            return ggmap.wrap_URL_in_html(s,'ChemID')
    except:
        pass
    return ''

def getChemIDImg(cas):
#    return f"""<center><img src="https://chem.nlm.nih.gov/chemidplus/structure/{cas}" width="120" alt="no image available from ChemID"/></center>"""
    return f"""<center><img src="https://chem.nlm.nih.gov/chemidplus/structure/{cas}" onerror="this.onerror=null; this.remove();" alt="" width="120"></center>"""


def getCompToxRef(DTXSID):
    #return DTXSID   
    try:
        if DTXSID[:3] == 'DTX':
            s = f'https://comptox.epa.gov/dashboard/dsstoxdb/results?search={DTXSID}'
            return ggmap.wrap_URL_in_html(s,'EPA: CompTox')
    except:
        pass
    return ""



def getMapLink(row,text_to_show='Analysis'):
    s = getLink(row)
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getAPIMapLink(row):
    s = getLink(row)
    return ggmap.wrap_URL_in_html(s,row.APINumber)


def xlate_to_str(inp,sep='; ',trunc=False,tlen=20,totallen = 5000,sort=True,
                maxlen=10000,maxMessage='Too many items to display'):
    try:
        if isinstance(inp,str):
            inp = [inp]
        l = list(inp)
        if sort:
            l.sort()
        if len(l)>maxlen:
            return maxMessage

        out = ''
        for a in l:
            s = str(a)
            if trunc:
                if len(s)>tlen:
                    s = s[:tlen-3]+ '...'
            out+= s+sep
        out = out[:-(len(sep))]
    except:
        return ''
    if len(out)>totallen:
        out = out[:totallen]+' ...' 
    return out

#############################  making folium maps #############################
import pandas as pd
import numpy as np
import geopandas as gpd
import folium

def get_state_center(state):
    t = pd.read_csv(r"C:\MyDocs\OpenFF\src\openFF-catalog\work\state_coords.csv",
                   dtype={'Latitude':'float', 'Longitude':'float'})
    t = t[t.state==state]
    #print(t)
    return [t.Latitude.mean(),t.Longitude.mean()*-1]

def fix_county_names(df):
    trans = {'mckenzie':'mc kenzie',
             'dewitt':'de witt',
             'mcclain':'mc clain',
             'mcintosh':'mc intosh',
             'mckean':'mc kean',
             'mcmullen':'mc mullen'}
    for wrong in trans.keys():
        df.CountyName = np.where(df.CountyName==wrong,trans[wrong],df.CountyName)
    return df

# single layer, with popups
def create_state_choropleth(data,
                            start_loc=[40, -96],start_zoom = 4,
                            custom_scale = [], plotlog = True,
                            legend_name = 'Test legend',
                            fields = ['StateName','orig_value'],
                            aliases = ['State: ','data: ']):
    fn = r"C:\MyDocs\OpenFF\data\non-FF\georef-united-states-of-america-state.geojson"
    geojson = gpd.read_file(fn)
    data['orig_value'] = data.value

    geojson['StateName'] = geojson.ste_name.str.lower()
    geojson = geojson[['StateName','ste_code','geometry']]
    #     geojson.drop(['ste_name'],axis=1,inplace=True)
    f = folium.Figure(width=600, height=400)
    m = folium.Map(location= start_loc, tiles="openstreetmap",
                    zoom_start=start_zoom).add_to(f)
#     fg1 = folium.FeatureGroup(name=legend_name,overlay=False).add_to(m)
    
    geojson = pd.merge(geojson,data,on=['StateName'],how='left')
    #geojson.value.fillna(0,inplace=True)
    if plotlog:
        geojson.value = np.log10(geojson.value+1)
        legend_name = legend_name + ' (log transformed)'
    geojson.orig_value.fillna('no data',inplace=True)
    
    if custom_scale==[]:
        custom_scale = (geojson['value'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
    folium.Choropleth(
                geo_data=fn,
                data=geojson,
                columns=['ste_code', 'value'],  #Here we tell folium to get the fips and plot values for each state
                key_on='feature.properties.ste_code',
                threshold_scale=custom_scale, #use the custom scale we created for legend
                fill_color='YlOrRd',
                nan_fill_color="gainsboro", #Use white color if there is no data available for the area
                fill_opacity=0.7,
                line_opacity=0.4,
                line_weight=0.3,
                legend_name= legend_name, #title of the legend
                highlight=True,
                line_color='black').add_to(m) 
    
    folium.features.GeoJson(
                data=geojson,
                name='',
                smooth_factor=2,
                style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                tooltip=folium.features.GeoJsonTooltip(
                    fields=fields,
                    aliases=aliases, 
                    localize=True,
                    sticky=False,
                    labels=True,
                    style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """,
                    max_width=800,),
                        highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                    ).add_to(m)   

    display(f)

def create_county_choropleth(data,
                             start_loc=[40, -96],start_zoom = 6,
                             custom_scale = [], plotlog = True,
                             legend_name = 'Test legend',
                             show_only_data_states=True,
                             #popup_enabled=True, tooltip_enabled=False,
                             fields = ['CountyName','orig_value'],
                             aliases = ['County: ','data: ']):
    fn = r"C:\MyDocs\OpenFF\data\non-FF\georef-united-states-of-america-county.geojson"
    if len(data)<1:
        print('No mappable data')
        return
    geojson = gpd.read_file(fn)
    data['orig_value'] = data.value

    geojson['StateName'] = geojson.ste_name.str.lower()
    geojson['CountyName'] = geojson.coty_name.str.lower()
    geojson = fix_county_names(geojson)
    working = geojson[['StateName','CountyName','coty_code','geometry']]
    #geojson = geojson.to_crs(5070)
    working = pd.merge(working,data,on=['StateName','CountyName'],how='left')
    #print(geojson.info())
    if start_loc==[]:
        start_loc = [geojson.geometry.centroid.x.mean(),geojson.geometry.centroid.y.mean()]
    f = folium.Figure(width=600, height=400)
    m = folium.Map(location= start_loc, tiles="openstreetmap",
                   zoom_start=start_zoom).add_to(f)
    if plotlog:
        working.value = np.log10(working.value+1)
        legend_name = legend_name + ' (log transformed)'
    working.orig_value.fillna('no data',inplace=True)
    
    if custom_scale==[]:
        custom_scale = (working['value'].quantile((0,0.2,0.4,0.6,0.8,1))).tolist()
    if show_only_data_states:
        gb = data.groupby(['StateName','CountyName'],as_index=False)['value'].first()
        datalst = []
        for i,row in gb.iterrows():
            datalst.append((row.StateName,row.CountyName))
        wlst = []
        working['tup'] = list(zip(working.StateName.tolist(),working.CountyName.tolist()))
        geojson['tup'] = list(zip(geojson.StateName.tolist(),geojson.CountyName.tolist()))
        
#         working = working[working.StateName.isin(data.StateName.unique().tolist())]
#         geojson = geojson[geojson.StateName.isin(data.StateName.unique().tolist())]
#         c1 = working.CountyName.isin(data.CountyName.unique().tolist())
#         c2 = working.StateName.isin(data.StateName.unique().tolist())
#         c3 = geojson.CountyName.isin(data.CountyName.unique().tolist())
#         c4 = geojson.StateName.isin(data.StateName.unique().tolist())
        working = working[working.tup.isin(datalst)]
        geojson = geojson[geojson.tup.isin(datalst)]
    working.StateName = working.StateName.str.title()
    working.CountyName = working.CountyName.str.title()
    #print(f'States in geojson: {working.StateName.unique().tolist()}')
    folium.Choropleth(
                geo_data=geojson,
                data=working,
                columns=['coty_code', 'value'],  #Here we tell folium to get the fips and plot values for each state
                key_on='feature.properties.coty_code',
                threshold_scale=custom_scale, #use the custom scale we created for legend
                fill_color='YlOrRd',
                nan_fill_color="gainsboro", #Use white color if there is no data available for the area
                fill_opacity=0.7,
                line_opacity=0.4,
                line_weight=0.4,
                legend_name= legend_name, #title of the legend
                highlight=True,
                line_color='black').add_to(m) 
    
    folium.features.GeoJson(
                data=working,
                name='',
                smooth_factor=2,
                style_function=lambda x: {'color':'black','fillColor':'transparent','weight':0.5},
                popup=folium.features.GeoJsonPopup(
                    fields=fields,
                    aliases=aliases, 
                    localize=True,
                    sticky=False,
                    labels=True,
                    style="""
                        background-color: #F0EFEF;
                        border: 2px solid black;
                        border-radius: 3px;
                        box-shadow: 3px;
                    """,
                    max_width=800,),
                        highlight_function=lambda x: {'weight':3,'fillColor':'grey'},
                    ).add_to(m)   

    display(f)
