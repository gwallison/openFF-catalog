"""catalog_common.py
Used as the first thing in all jupyter index files.
This is the first thing executed.
"""
import datetime
from IPython.display import Markdown as md
from IPython.core.display import display, HTML

repo_name = 'v11_BETA_2021-12-18'
bulkdata_date = 'December 18, 2021'
cat_creation_date = datetime.datetime.now()
extData_loc = 'c:/MyDocs/OpenFF/data/external_refs/'
transformed_loc = 'c:/MyDocs/OpenFF/data/transformed/'


def ID_header():
    display(md(f"""Download from FracFocus: **{bulkdata_date}**; Data repository: **{repo_name}**; This file generated: **{cat_creation_date:%B %d, %Y}**."""))

###############################  Used to make repository accessible ####################
import sys
sys.path.insert(0,'c:/MyDocs/OpenFF/src/')
import common.code.Analysis_set_remote as ana_set
import common.code.get_repo_data as grd
import common.code.get_google_map as ggmap

# #############################  Make indices full page ###################################
# display(HTML("<style>.container { width:100% !important; }</style>"))


###########################  for itables #####################################
# this code is necessary to keep itables working with new ngcovert templates
from IPython.display import HTML, display
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

def getDataLink(cas):
    s = f'{cas}/data.csv'
    return ggmap.wrap_URL_in_html(s,'csv file')

def getChemIDLink(cas):
    s = f'https://chem.nlm.nih.gov/chemidplus/rn/{cas}'
    return ggmap.wrap_URL_in_html(s,'ChemID')

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
        return "<no EPA link>"



def getMapLink(row,text_to_show='Analysis'):
    s = getLink(row)
    return ggmap.wrap_URL_in_html(s,text_to_show)

def getAPIMapLink(row):
    s = getLink(row)
    return ggmap.wrap_URL_in_html(s,row.APINumber)

# def xlate_to_str(inp,sep=' ',trunc=False,tlen=20,totallen = 5000):
#     try:
#         l = list(inp)
#         out = ''
#         for s in l:
#             if trunc:
#                 if len(s)>tlen:
#                     s = s[:tlen-3]+ '...'
#             out+= s+sep
#     except:
#         return ''
#     return out[:-(len(sep))]

def xlate_to_str(inp,sep='; ',trunc=False,tlen=20,totallen = 5000,
                maxlen=10000,maxMessage='Too many items to display'):
    try:
        l = list(inp)
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


########################### To execute at the top of the file
ID_header()