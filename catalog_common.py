"""catalog_common.py
Used as the first thing in all jupyter index files.
This is the first thing executed.

Passing arguments in:
sys.argv:
0 = this scripts name
1 = header title - no spaces! use '_' to indicate spaces
"""
import datetime
import time
import sys
import os
from IPython.display import Markdown as md
# from IPython.core.display import display, HTML
from IPython.display import display, HTML

# itables allow interactive tables but also require downloading html to view
use_itables = True

if use_itables:
    from itables import init_notebook_mode
    init_notebook_mode(all_interactive=True)
    from itables import show as iShow
    import itables.options as opt
    opt.classes="display compact cell-border"
    opt.maxBytes = 0
    
else:
    def iShow(df,maxBytes=0,classes=None):
        display(df)


import warnings
warnings.filterwarnings('ignore')


repo_name = 'openFF_data_2023_11_25'
catalog_ver = '0.1.0'
#repo_name = 'SkyTruth_2022_09_11'
data_source = 'bulk'  # can be 'bulk', 'FFV1_scrape' or 'SkyTruth'
                                    # or 'NM_scrape_2022_05'

bulkdata_date = 'November 25, 2023'
cat_creation_date = datetime.datetime.now()
extData_loc = 'c:/MyDocs/OpenFF/data/external_refs/'
transformed_loc = 'c:/MyDocs/OpenFF/data/transformed/'
pic_dir = r"C:\MyDocs\OpenFF\src\openFF-catalog\pic_dir"

def data_banner():
    # used to alert user when catalog in NOT of official bulk resource
    if data_source=='bulk':
        return  ''
    else:
        s = f""" <center><H2>ATTENTION:<br>
        This catalog page is not based on the official FracFocus download<br>
        but an alternative data set:</H2><H1>** {data_source} **</H1>
        Please be aware of the caveats for these data. <br>
        Some sections of the catalog may not be appropriate.</center><br><br><hr>
        """
        display(HTML(s))
        
def ID_header(title = '',line2 ='', subtitle = '',imagelink='',
              incl_links=True,link_up_level=False,
              show_source=True):

    data_banner()
    local_prefix = ''
    if link_up_level:
        local_prefix= '../'
        
    logo = """<a href="https://frackingchemicaldisclosure.wordpress.com/" title="Open-FF home page, tour and blog"><img src="https://storage.googleapis.com/open-ff-common/openFF_logo.png" alt="openFF logo" width="100" height="100"></a>"""
    logoFT = """<center><a href="https://www.fractracker.org/" title="FracTracker Alliance"><img src="https://storage.googleapis.com/open-ff-common/2021_FT_logo_icon.png" alt="FracTracker logo" width="100" height="100"><br>Sponsored by FracTracker Alliance</a></center>"""

    if show_source:
        source = f"""This file was generated on {cat_creation_date:%B %d, %Y} <br>from data repository: {repo_name} with code version:  {catalog_ver}."""
    else:
        source = ''
    # cat_links = f"""<td width=20%>
    #                 <p style="text-align: center; font-size:120%"> 
    #                   <a href="{local_prefix}Open-FF_Catalog.html" title="Local Navigator"> Navigator Page </a>|
    #                   <a href="{local_prefix}Open-FF_Chemicals.html" title="OpenFF Chemical index"> Chemical Index </a>|
    #                   <a href="{local_prefix}Open-FF_States_and_Counties.html" title="OpenFF States index"> State Index </a>|
    #                   <a href="{local_prefix}Open-FF_Operator_Index.html" title="OpenFF Operator index"> Operator Index </a>
    #                   <a href="https://frackingchemicaldisclosure.wordpress.com/" title="Open-FF home page, tour and blog"> Open-FF Home </a><br>
    #                 </p>
    #                 </td>
    #             """
    cat_links = f"""<p style="text-align: center; font-size:100%"> Links: 
                      <a href="{local_prefix}Open-FF_Catalog.html" title="Local Navigator"> Navigator Page </a>|
                      <a href="{local_prefix}Open-FF_Chemicals.html" title="OpenFF Chemical index"> Chemical Index </a>|
                      <a href="{local_prefix}Open-FF_States_and_Counties.html" title="OpenFF States index"> State Index </a>|
                      <a href="{local_prefix}Open-FF_Operator_Index.html" title="OpenFF Operator index"> Operator Index </a>
                    </p>
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
                </style>{cat_txt}<hr>
                <table style='margin: 0 auto' >
                <tr>
                <td width=15%>{logo}</td>
                <td><p style="text-align: center; font-size:300%">{title}</p><br> {line2_alt} {subtitle_alt} {image_alt}
                    <p style="text-align: center; font-size:100%">{source}
                </td>
                <td width=15%>{logoFT}</td>
                </tr>
            </table><hr>"""
    display(HTML(table))

def displaySource():
    source = f"""This file generated on {cat_creation_date:%B %d, %Y} from data repository: {repo_name}."""
    display(HTML(source))

def setup_collapsibles():
    display(HTML("""<style>
.collapsible {
  background-color: #777;
  color: white;
  cursor: pointer;
  padding: 18px;
  width: 80%;
  border: none;
  text-align: left;
  outline: none;
  font-size: 15px;
}

.active, .collapsible:hover {
  background-color: #555;
}

.content {
  padding: 0 18px;
  display: none;
  overflow: hidden;
  background-color: #f1f1f1;
}
</style>

"""))
    
def addCollapJS():
    display(HTML("""<script>
var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.display === "block") {
      content.style.display = "none";
    } else {
      content.style.display = "block";
    }
  });
}
</script>"""))
    
    
def insert_collapsible(displayed='Read More...', content='stuff'):
    display(HTML(f"""<button type="button" class="collapsible">{displayed}</button>
<div class="content">
  <p>{content}</p>
</div>
"""))
    addCollapJS()

# def show_mod_footer(filepath,repo=repo_name):
#     display(md(f"""The code for this webpage was last revised **{time.ctime(os.path.getmtime(filepath))}** and the data were compiled from the **{repo}** repository."""))
    
###############################  Used to make repository accessible ####################
#import sys
sys.path.insert(0,'c:/MyDocs/OpenFF/src/')
import common.code.Analysis_set_remote as ana_set
import common.code.Analysis_set_remote_old as ana_set_old # to fetch older repos
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
def round_sig(x, sig=2,guarantee_str=''):
    try:
        if abs(x)>=1:
            out =  int(round(x, sig-int(floor(log10(abs(x))))-1))
            return f"{out:,d}" # does the right thing with commas
        else: # fractional numbers
            return str(round(x, sig-int(floor(log10(abs(x))))-1))
    except:
        if guarantee_str:
            return guarantee_str
        return x
    
# used to insert links of google maps into tables
def make_clickable(val):
    try:
        if val[:4]=='http':
            return '<a href="{}" target="_blank">{}</a>'.format(val,'map')
    except:
        return val
    return val

def getLink(row,latname='bgLatitude',lonname='bgLongitude'):
    return ggmap.getSearchLink(row[latname],row[lonname])
#    return ggmap.getSearchLink(row.bgLatitude,row.bgLongitude)

def getCatLink(cas,text_to_show='Analysis',use_remote=False):
    preamble = ''
    if use_remote:
        preamble = 'https://storage.googleapis.com/open-ff-browser/'
    s = f'{preamble}{cas}/analysis_{cas}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getOpLink(opname,text_to_show='Operator details',use_remote=False,up_level=False):
    preamble = ''
    if use_remote:
        preamble = 'https://storage.googleapis.com/open-ff-browser/'
    if up_level:
        preamble = '../'
    s = f'{preamble}operators/{opname}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getStateLink(state,text_to_show='State details',use_remote=False):
    preamble = 'states'
    if use_remote:
        preamble = 'https://storage.googleapis.com/open-ff-browser/states/'
    s = f'{preamble}/{state.lower()}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getCountyLink(county,state,text_to_show='County details',use_remote=False):
    preamble = '.' # when coming from a state link, don't need preamble
    if use_remote:
        preamble = 'https://storage.googleapis.com/open-ff-browser/states/'
    name = county.lower().replace(' ','_') + '-' + state.lower().replace(' ','_')
    # s = f'{preamble}/{name}.csv'
    s = f'{preamble}/{name}.html'
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getDataLink(cas):
    s = f'{cas}/data.zip'
    return ggmap.wrap_URL_in_html(s,'data; ')

def wrapLink(url,txt):
    # simple wrapping to make a link displayable in notebook
    return ggmap.wrap_URL_in_html(url,txt)

#  CHEMID is no longer running
# def getChemIDLink(cas):
#     try:
#         if cas[0] in ['0','1','2','3','4','5','6','7','8','9']:
#             s = f'https://chem.nlm.nih.gov/chemidplus/rn/{cas}'
#             return ggmap.wrap_URL_in_html(s,'ChemID; ')
#     except:
#         pass
#     return ''

# def getChemIDImg(cas):
# #    return f"""<center><img src="https://chem.nlm.nih.gov/chemidplus/structure/{cas}" width="120" alt="no image available from ChemID"/></center>"""
#     return f"""<center><img src="https://chem.nlm.nih.gov/chemidplus/structure/{cas}" onerror="this.onerror=null; this.remove();" alt="" width="120"></center>"""

def getPubChemLink(cas):
    try:
        if cas[0].isnumeric():
            s = f'https://pubchem.ncbi.nlm.nih.gov/#query={cas}'
            return ggmap.wrap_URL_in_html(s,'PubChem; ')
    except:
        pass
    return ''

def getMoleculeImg(cas,size=120,chemical_report=False):
    prefix = ''
    if chemical_report: prefix='../'
    ct_path = os.path.join(pic_dir,cas,'comptoxid.png')
    # take comptox version if it exists
    if os.path.exists(ct_path):
        # and is not empty:  # this is the normal return
        if os.path.getsize(ct_path) > 0:
            return f"""<center><img src="{prefix}images/{cas}/comptoxid.png" onerror="this.onerror=null; this.remove();" width="{size}"></center>"""
    else: # but if all else fails, try linking ot chemid
        ci_path = os.path.join(pic_dir,cas,'chemid.png')
        if os.path.exists(ci_path):
            if os.path.getsize(ci_path) > 0:
                return f"""<center><img src="{prefix}images/{cas}/chemid.png" onerror="this.onerror=null; this.remove();" width="{size}"></center>"""
    return "<center>Image not available</center>"

            
def getMoleculeImgBig(cas):
    return f"""<center><img src="../images/{cas}/comptoxid.png" onerror="this.onerror=null; this.remove();" width="300"></center>"""

def getFingerprintImg(cas):
    fp_path = os.path.join(pic_dir,cas,'haz_fingerprint.png')
    # take comptox version if it exists
    if os.path.exists(fp_path):
        return f"""<center><img src="images/{cas}/haz_fingerprint.png" onerror="this.onerror=null; this.remove();" width="200"></center>"""
    return "<center>ChemInformatics not available</center>"
    
def getCompToxRef(DTXSID):
    #return DTXSID   
    try:
        if DTXSID[:3] == 'DTX':
            s = f'https://comptox.epa.gov/dashboard/dsstoxdb/results?search={DTXSID}'
            return ggmap.wrap_URL_in_html(s,'CompTox')
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


##########  getting some basic lists from the repository

def get_cas_list():
    """returns list of all bgCAS numbers in current repository"""
    repoloc = r"C:\MyDocs\OpenFF\data\repos/"+repo_name
    pkl = pd.read_parquet(os.path.join(repoloc,'pickles/bgCAS.parquet'))
    #pkl.to_csv('./tmp/bgCAS.csv')
    lst = pkl.bgCAS.str.strip().unique().tolist()
    for cas in lst:
        if (cas[-1]==' ')|(cas[0]==' '):
            print(f'CAS list error: <<{cas}>>')
    return lst


def get_comptox_df():
    """returns df of bgCAS with DTXSID ids as well as bgCAS"""
    repoloc = r"C:\MyDocs\OpenFF\data\repos/"+repo_name
    pkl = pd.read_parquet(os.path.join(repoloc,'pickles/bgCAS.parquet'))
    #print(f'Len dtxsid: {pkl.DTXSID.notna().sum()}, {len(pkl)}')
    #print(f'{pkl[["bgCAS","DTXSID"]].head(10)}')
    print('CAS without DTXSID:')
    print(pkl[pkl.DTXSID.isna()].bgCAS.tolist())
    return pkl[pkl.DTXSID.notna()][['bgCAS','DTXSID']]

    
 
    

#############################  making folium maps #############################
import pandas as pd
import numpy as np
import geopandas as gpd
import folium
from folium import plugins
final_crs = 4326 # WGS84

def get_state_center(state):
    t = pd.read_csv(r"C:\MyDocs\OpenFF\src\openFF-catalog\work\state_coords.csv",
                   dtype={'Latitude':'float', 'Longitude':'float'})
    t = t[t.state==state]
    #print(t)
    return [t.Latitude.mean(),t.Longitude.mean()*-1]

def get_geog_center(state_list):
    t = pd.read_csv(r"C:\MyDocs\OpenFF\src\openFF-catalog\work\state_coords.csv",
                   dtype={'Latitude':'float', 'Longitude':'float'})
    t = t[t.state.isin(state_list)]
    #print(t)
    return [t.Latitude.mean(),t.Longitude.mean()*-1]

def get_zoom_level(df):
    latdiff = df.bgLatitude.max() - df.bgLatitude.min()
    londiff = df.bgLongitude.max()- df.bgLongitude.min()
    #print(f'latdiff = {latdiff}, londiff = {londiff}')
    diffsum = latdiff+londiff
    if diffsum <1 : return 6
    if diffsum <5 : return 5
    if diffsum <20 : return 4
    if diffsum <28 : return 3.5
    return 3
    

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

def create_point_map(data,include_mini_map=False,include_shape=False,area_df=None,
                     fields=['APINumber','TotalBaseWaterVolume','year','OperatorName','ingKeyPresent'],
                     aliases=['API Number','Water Volume','year','Operator','has chem recs'],
                     width=600,height=400):
    # only the first item of the area df is used.  Meant to be a simple outline
    
    f = folium.Figure(width=width, height=height)
    if include_shape:
        #print('including shape!')
        area = [area_df.centroid.geometry.y.iloc[0],area_df.centroid.geometry.x.iloc[0]]
        m = folium.Map(tiles="openstreetmap",location=area, zoom_start=10).add_to(f)
        
        # show area
        style = {'fillColor': '#00000000', 'color': '#0000FFFF'}
        folium.GeoJson(area_df,
                       style_function=lambda x: style,
                       smooth_factor=.2,
                       name= 'target area'
                       ).add_to(m)


    else:
        m = folium.Map(tiles="openstreetmap").add_to(f)
    locations = list(zip(data.bgLatitude, data.bgLongitude))
    cluster = plugins.MarkerCluster(locations=locations,
                                   name='cluster markers')#,                     
    m.add_child(cluster)
    
    sw = data[['bgLatitude', 'bgLongitude']].min().values.tolist()
    ne = data[['bgLatitude', 'bgLongitude']].max().values.tolist()
    m.fit_bounds([sw, ne]) 

    gdf = gpd.GeoDataFrame(data, geometry=gpd.points_from_xy(data.bgLongitude,
                                                            data.bgLatitude),
                           crs=final_crs)
    folium.features.GeoJson(
            data=gdf,
            name='information marker',
            show=False,
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
    
    # Add a tile layer with satellite imagery
    folium.TileLayer(
        tiles='https://{s}.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite',
        overlay=False,
        control=True,
        subdomains=['mt0', 'mt1', 'mt2', 'mt3']
    ).add_to(m)

    # Add layer control to switch between base maps
    folium.LayerControl().add_to(m)

    if include_mini_map:
        minimap = plugins.MiniMap()
        m.add_child(minimap)
        

    display(f)



# single layer, with popups
def create_state_choropleth(data,
                            start_loc=[40, -96],start_zoom = 4,
                            custom_scale = [], plotlog = True,
                            legend_name = 'Test legend',
                            fields = ['StateName','orig_value'],
                            aliases = ['State: ','data: '],
                            width=600,height=400):
    fn = r"C:\MyDocs\OpenFF\data\non-FF\georef-united-states-of-america-state.geojson"
    geojson = gpd.read_file(fn)
    data['orig_value'] = data.value

    geojson['StateName'] = geojson.ste_name.str.lower()
    geojson = geojson[['StateName','ste_code','geometry']]
    #     geojson.drop(['ste_name'],axis=1,inplace=True)
    f = folium.Figure(width=width, height=height)
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
# fit_bounds needs work: https://stackoverflow.com/questions/58162200/pre-determine-optimal-level-of-zoom-in-folium
#     sw = data[['bgLatitude', 'bgLongitude']].min().values.tolist()
#     ne = data[['bgLatitude', 'bgLongitude']].max().values.tolist()

#     m.fit_bounds([sw, ne]) 
    display(f)

if __name__ == '__main__':
    df = get_cas_list()