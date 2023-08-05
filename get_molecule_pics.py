# -*- coding: utf-8 -*-
"""
Created on Wed Sep  7 20:23:03 2022

@author: Gary
"""

import os
import time
import requests

from catalog_common import get_cas_list, get_comptox_df

pic_dir = 'c:/MyDocs/OpenFF/src/openFF-catalog/pic_dir/'


def make_pic_dir(caslst=['50-00-0']):
    try:
        lst = os.listdir(pic_dir)
    except:
        print('Creating new pic directory')
        os.mkdir(pic_dir)
    for cas in caslst:
        d = os.path.join(pic_dir,cas)
        if not os.path.exists(d):
            print(f'making dir: {cas}')
            os.mkdir(d)
            
#  ChemID has been deprecated. PubChem instead and images are fetched manually    
# def fetch_chem_id_pic(cas):
#     url = f"https://chem.nlm.nih.gov/chemidplus/structure/{cas}" 
#     rq = requests.get(url,timeout=100)
#     if rq.status_code==200:
#         print(f'ChemID: {cas} - got it!')
#         with open(os.path.join(pic_dir,cas,'chemid.png'),'wb') as f:
#             f.write(rq.content)
#     else:
#         if rq.status_code==404:
#             with open(os.path.join(pic_dir,cas,'chemid.png'),'wb') as f:
#                 f.write(b'')
#             print(f'{cas} - 404')
#         else:
#             print(f'{cas} {rq.status_code}: what happened?')

def fetch_comptox_pic(cas,dtxsid):
    url = f"https://comptox.epa.gov/dashboard-api/ccdapp1/chemical-files/image/by-dtxsid/{dtxsid}"    
    rq = requests.get(url,timeout=1000)
    if rq.status_code==200:
        print(f'Comptox: {cas} - found it!')
        path = os.path.join(pic_dir,cas,'comptoxid.png')
        with open(path,'wb') as f:
            f.write(rq.content)
        if os.path.getsize(path)==0: # empty files returned when they don't exist
            print('... but it is empty')
            #os.remove(path)  # KEEP empty file as signal

    else:
        if rq.status_code==404:
            print(f'{cas} - 404')
        else:
            print(f'{cas} {rq.status_code}: what happened?')
    

## depending on empty file to signal no image at comptox, to prevent searching
##   every time.  Don't use cleanup regularly!!

# def cleanup_dirs(caslst):
#     for cas in caslst:
#         path = os.path.join(pic_dir,cas,'comptoxid.png')
#         if os.path.exists(path):
#             if os.path.getsize(path) == 0:
#                 print(f'removing empty file for {cas}')
#                 os.remove(path)
                
def show_chemID_only(caslst):
    """finds and lists those cas numbers that don't have comptox images"""
    for cas in caslst:
        ctpath = os.path.join(pic_dir,cas,'comptoxid.png')
        cidpath = os.path.join(pic_dir,cas,'chemid.png')
        if not os.path.exists(ctpath):
            if os.path.exists(cidpath):
                print(cas)
    
if __name__ == '__main__':
    caslst = get_cas_list()        
    dtxdf = get_comptox_df()
    # print(dtxdf.columns)
    make_pic_dir(caslst=caslst)
    #show_chemID_only(caslst)

    # for cas in caslst:
    #     if not os.path.exists(os.path.join(pic_dir,cas,'chemid.png')):
    #         #print(f'<<{cas}>>')
    #         fetch_chem_id_pic(cas)
    #         time.sleep(8)

    for i,row in dtxdf.iterrows():
        #print(row.DTXSID)
        if not os.path.exists(os.path.join(pic_dir,row.bgCAS,'comptoxid.png')):
            print(f'trying to fetch: {row.bgCAS}')
            if row.DTXSID[:3]=='DTX':
                fetch_comptox_pic(row.bgCAS, row.DTXSID)
                time.sleep(5)

      
    
