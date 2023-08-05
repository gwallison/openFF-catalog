# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 09:19:51 2023

@author: garya

to create the reports:

    - currently need to break the list into chunks of about 100 chem. One report per each chunk
    - Take chunk of DTXSID (or casrn) and feed into ChemInformatics. Click on "Hazards"
    - "Search Chemicals to add to ChemCart". After searching make sure to click "Add to ChemCart"
    - Click on the cart icon to generate the report
    - Download report as XLSX; store in report directory.
    - Make sure that the variables are still in the same position as the previous download. The routines depend on a particular order
"""
import pandas as pd
import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from IPython.display import display
from IPython.display import Markdown as md

from catalog_common import get_cas_list


# from IPython.display import display,HTML
# from IPython.display import Markdown as md

report_dir = r"C:\MyDocs\OpenFF\data\external_refs\ChemInformatics"
im_dir = r"C:\MyDocs\OpenFF\src\openFF-catalog\pic_dir"


lst = os.listdir(report_dir)
#print(lst)
def get_summary_from_xls(fn):
    """This routine throws a warning for each file in the report dir. They are
    harmless and difficult to remove."""
    t = pd.read_excel(fn,skiprows=5)
    cols = ['DTXSID','CASRN','Name','HH: Oral','HH: Inhalation','HH: Dermal','HH: Carcinogenicity',
            'HH: Genotoxicity Mutagenicity','HH: Endocrine Disruption','HH: Reproductive','HH: Developmental',
            'HH: Neurotoxicity: Repeat Exposure','HH: Neurotoxicity: Single Exposure',
            'HH: Systemic Toxicity: Repeat Exposure','HH: Systemic Toxicity: Single Exposure',
            'HH: Skin Sensitization','HH: Skin Irritation','HH: Eye Irritation','Ecotoxicity: Acute Aquatic Toxicity','Ecotoxicity: Chronic Aquatic Toxicity',
            'Fate: Persistence','Fate: Bioaccumulation','Fate: Exposure']
    t.columns = cols
    return t

def get_all():
    dfs = []
    for fn in lst:
        filename = os.path.join(report_dir,fn)
        dfs.append(get_summary_from_xls(filename))
    out = pd.concat(dfs,sort=False)
    #print(len(out))
    out = out[~out.duplicated(subset='DTXSID')]
    #print(len(out))
    return out


# # create the pandas style version
# def add_style(v,props=''):
#     #print(s)
#     if v=='VH':return 'text-align: center;background-color:red'
#     if v=='H':return 'text-align: center;background-color:orange'
#     if v=='M':return 'text-align: center;background-color:yellow'
#     if v=='L':return 'text-align: center;background-color:lightgreen'
#     if v=='I':return 'text-align: center;background-color:lightgrey'
#     if v=='ND':return 'text-align: center;background-color:darkgrey'

#     return ''

# def make_style(df,casrn = '50-00-0'): # just one   
#     df = df[df.CASRN==casrn].drop(['Name','DTXSID'],axis=1)
#     if len(df)>0:
#         # don't make a file when no data available
#         df = df.fillna('ND')
#         df.reset_index(drop=True,inplace=True)
#         t = df.set_index('CASRN').T
#         display(t.style.applymap(add_style))
#         # out.to_pickle(os.path.join(im_dir,casrn,'haz_df.pkl'))
#     else:
#         display(md('#### No analysis available'))

def getImage(path, zoom=.5):
    return OffsetImage(plt.imread(path), zoom=zoom)

def make_fingerprint(df,casrn = '107-19-7'):
    #print(casrn)
    t = df[df.CASRN==casrn].drop(['DTXSID','CASRN','Name'],axis=1)
    t = t.fillna('ND')
    #categ = ['VH','H','M','L','I','ND']
    im_dic = {'I':os.path.join(im_dir,'ci_icons','grey_question.png'),
              'ND':os.path.join(im_dir,'ci_icons','grey_square.png'),
              'H':os.path.join(im_dir,'ci_icons','orange_exclamation.png'),
              'VH':os.path.join(im_dir,'ci_icons','red_skull.png'),
              'M':os.path.join(im_dir,'ci_icons','yellow-minus.png'),
              'L':os.path.join(im_dir,'ci_icons','green-minus.png'),
              'noval':os.path.join(im_dir,'ci_icons','brown-x.png')}

    out = t.values.flatten().tolist()
    
    # handle chem without ci data
    if len(out) == 0: # don't save anything
        #for i in range(20): out.append('noval') 
        return
    x = []; y = []; paths = []          
    for i,val in enumerate(out):
        x.append(i%5)
        y.append(3 - i//5)
        paths.append(im_dic[val])
    # for i in zip(x, y,paths): print(i)
    fig, ax = plt.subplots(facecolor='black')
    ax.scatter(x, y) 
    # ax.set_title(casrn)

    for x0, y0, path in zip(x, y,paths):
        ab = AnnotationBbox(getImage(path,zoom=0.75), (x0, y0), frameon=False)
                           # bboxprops = dict(facecolor='wheat',boxstyle='round',color='black'))
        ax.add_artist(ab)
        ax.set_facecolor('black')
    plt.savefig(os.path.join(im_dir,casrn,'haz_fingerprint.png'))    

def make_all_fingerprints(caslst,hazdf):
    cas_ignore = ['proprietary','ambiguousID','sysAppMeta','conflictingID']
    for i,cas in enumerate(caslst):
        print(f'{i}: {cas}')
        if not cas in cas_ignore:            
            make_fingerprint(hazdf,cas)
        
def remove_all(caslst):
    for cas in caslst:
        try:
            os.remove(os.path.join(im_dir,cas,'haz_fingerprint.png'))        
        except:
            print(f'Not there: {cas}')
            
            
if __name__ == '__main__':
    caslst = get_cas_list()        
    out = get_all()
    make_all_fingerprints(caslst=caslst,hazdf=out)
    print('Done')
    # remove_all(caslst)
