# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:05:07 2020

@author: Gary
"""

# 
import os,sys
sys.path.insert(0,'c:/MyDocs/OpenFF/src/')
from common.code import Analysis_set_remote as ana_set
from common.code import get_google_map as ggmap

work_pickles = 'c:/MyDocs/OpenFF/src/common/'

import numpy as np
import pandas as pd
import shutil
import subprocess
from datetime import datetime
import pickle

today = datetime.today()

# for nicer displays of numbers: round to significant figures.
from math import log10, floor
def round_sig(x, sig=2):
    try:
        return int(round(x, sig-int(floor(log10(abs(x))))-1))
    except:
        return x

class Web_gen():
    
    def __init__(self,repo_name = 'unknown',data_date='UNKNOWN',caslist = []):
        self.repo_name = repo_name
        self.data_date = data_date
        self.outdir = './out/website/'
        self.scopedir = self.outdir+'./scope/'
        self.css_fn = './work/style.css'
        #self.default_empty_fn = './website_gen/default_empty.html'
        self.jupyter_fn = './work/chemical_report.html'
        self.ref_fn = './work/ref.csv'
        self.filtered_fields = ['PercentHFJob', 
                                'calcMass', 'UploadKey', 'OperatorName',
                                'bgOperatorName',
                                'APINumber', 'TotalBaseWaterVolume',
                                'TotalBaseNonWaterVolume', 'FFVersion', 
                                'TVD', 'StateName', 'StateNumber', 'CountyName', 
                                'CountyNumber', 'TradeName',
                                'Latitude', 'Longitude', 'Projection',
                                'data_source', 'bgStateName', 'bgCountyName', 
                                'bgLatitude', 'bgLongitude', 'date',
                                'IngredientName', 'Supplier', 'bgSupplier', 
                                'Purpose', 'CASNumber', 'bgCAS','primarySupplier',
                                'bgIngredientName','in_std_filtered',
                                'TradeName_trunc','Purp_trunc','has_TBWV',
                                'within_total_tolerance','has_water_carrier',
                                'carrier_status','massComp','massCompFlag'] 
        self.caslist = caslist
        self.allrec = ana_set.Catalog_set(repo = self.repo_name,
                                          force_new_creation=True,
                                          outdir=work_pickles).get_set()
        #print(f'allrec len {len(self.allrec)}')
        self.allrec['TradeName_trunc'] = np.where(self.allrec.TradeName.str.len()>30,
                                                  self.allrec.TradeName.str[:30]+'...',
                                                  self.allrec.TradeName)
        self.allrec['Purp_trunc'] = np.where(self.allrec.Purpose.str.len()>30,
                                                  self.allrec.Purpose.str[:30]+'...',
                                                  self.allrec.Purpose)
# =============================================================================
#         # use this to make shortened versions
#         if caslist != []:
#             self.allrec = self.allrec[self.allrec.bgCAS.isin(caslist)]
# =============================================================================
        w_chem = ~(self.allrec.no_chem_recs)
        filtered = self.allrec.in_std_filtered
        self.num_events = len(self.allrec.UploadKey.unique())
        self.num_events_wo_FFV1 = len(self.allrec[w_chem].UploadKey.unique())
        self.num_events_fil = len(self.allrec[filtered].UploadKey.unique())
        self.num_events_fil_wo_FFV1 = len(self.allrec[filtered & w_chem].UploadKey.unique())

        
    def initialize_dir(self,dir):
        shutil.rmtree(dir,ignore_errors=True)
        os.mkdir(dir)
                      
    def make_dir_structure(self,caslist=[]):
        self.initialize_dir(self.outdir)
        self.initialize_dir(self.scopedir)
        #for cas in caslist:
        #    self.initialize_dir(self.outdir+cas)
        shutil.copyfile(self.css_fn,self.outdir+'style.css')

    def compile_page(self,title='empty title',header='',body=''):
        return f"""<!DOCTYPE html>
<html>
  <head>
    <title>{title}</title>
    <link rel='stylesheet' href='style.css' />
  </head>
  <body>
      <h1>{header}</h1>
      <h4>Data cleaned and extracted from <a href=https://www.FracFocus.org >FracFocus</a>, downloaded on {self.data_date}</h4>
    {body}
  </body>
</html>
"""
    def save_page(self,webtxt='', fn='index.html'):
        with open(self.outdir+fn,'w') as f:
            f.write(webtxt)
    
    def add_table_line(self,vals=[]):
        s = '  <tr>\n'
        for item in vals:        
            s+= f'    <td> {item} </td> \n'
        s+= '   </tr>\n'
        return s
    
    def add_table_head(self,vals=[]):
        s = '  <tr>\n'
        for item in vals:        
            s+= f'    <th> {item} </th> \n'
        s+= '   </tr>\n'
        return s

    def save_global_vals(self,num_UploadKey=None,cas='?',
                         IngredientName='?',eh_IngredientName='?'):
        """put numbers used by all analyses into a file for access
        within Jupyter scripts."""
        vname = ['tot_num_disc','tot_num_disc_less_FFV1',
                 'tot_num_disc_fil','tot_num_disc_fil_less_FFV1',
                 'data_date','today','target_cas']
        vals = [self.num_events,self.num_events_wo_FFV1,
                self.num_events_fil,self.num_events_fil_wo_FFV1,
                self.data_date,today,cas]
        pd.DataFrame({'varname':vname,'value':vals}).to_csv(self.ref_fn,
                                                            index=False)

    def make_map_link(self,row):
        l = ggmap.getSearchLink(lat=row.bgLatitude,lon=row.bgLongitude)
        return ggmap.wrap_URL_in_html(l,'map')
            
    def make_bgCAS_name_df(self,namedf):
        fns = ['Chemical Abstracts Index Name5521926666129599114.csv',
              'Chemical Abstracts Index Name6033273653638177995.csv']
        epa0 = pd.read_csv('./work/'+fns[0],low_memory=False)
        epa1 = pd.read_csv('./work/'+fns[1],low_memory=False)
        epa = pd.concat([epa0,epa1],sort=True)
        epa = epa.rename({'CAS #':'bgCAS'},axis=1)
        namedf = pd.merge(namedf,epa,on='bgCAS',how='left')
        namedf = namedf.rename({'Registry Name':'epa_Registry_Name',
                                'Substance Name':'epa_Substance_Name'},axis=1)
        namedf['eh_IngredientName'] = ''
        namedf[['bgCAS','bgIngredientName','eh_IngredientName',
                'epa_Registry_Name','epa_Substance_Name']].to_csv('./work/bgCAS.csv',
                                                                  encoding='utf-8',
                                                                  index=False)
    def make_chem_list(self):
        t = self.allrec
        if self.caslist != []: # then do all
            t = t[t.bgCAS.isin(self.caslist)]
        gb = t.groupby('bgCAS',as_index=False)[['bgIngredientName']].first()
        self.make_bgCAS_name_df(gb)
        #gb = gb[:4]  #limit length for development
        lst = gb.bgCAS.unique().tolist()
        lst.sort()
        self.make_dir_structure(lst)
        #print(gb[440:450])
        
        for (i, row) in gb.iterrows():
            #if i>15:  # control the overall list
            #    continue # skip the rest
            chem = row.bgCAS
            self.initialize_dir(self.outdir+chem)

            #ingred = row.bgIngredientName
            self.save_global_vals(self.num_events,chem,
                                  row.bgIngredientName)
            
            tt = self.allrec[self.allrec.bgCAS==chem]
            tt = tt.filter(self.filtered_fields,axis=1).copy()
            # re-run the non-mass ones
            #if tt.bgMass.max() >0:
            #    continue
            mx = round_sig(tt.calcMass.max())
            print(f'{i}: ** {chem:>13} **  n recs: {len(tt):>7,}; max mass: {mx:>10,}')
            
            if len(tt)>0:
                tt['map_link'] = tt.apply(lambda x: self.make_map_link(x),axis=1)
            else:
                tt['map_link'] = ''
            # save data to file for later notebook access
            tt.to_csv('work/data.csv',index=False)
            tt.to_csv(self.outdir+chem+'/data.csv',index=False)
            self.make_jupyter_output()
            self.fix_html_title(chem)
            an_fn = f'/analysis_{chem}.html'
            shutil.copyfile(self.jupyter_fn,self.outdir+chem+an_fn)
            
    def make_scope_data(self):
        # prepare the downloadable data sets
        print('  -- working on scope data sets')
        # water and sand data
        gb1 = self.allrec[self.allrec.in_std_filtered].groupby('UploadKey',as_index=False)\
            [['TotalBaseWaterVolume','date','OperatorName','bgOperatorName',
             'StateName','CountyName','APINumber','Latitude','Longitude']].first()
        gb1['api10'] = gb1.APINumber.str[:10]
        cond = self.allrec.bgCAS=='14808-60-7'
        gb2 = self.allrec[cond&(self.allrec.in_std_filtered)].groupby('UploadKey',as_index=False)\
            ['calcMass'].sum().rename({'calcMass':'sandMass'},axis=1)
        out = pd.merge(gb1,gb2,on='UploadKey',how='left')
        out.drop('UploadKey',axis=1,inplace=True)
        out.to_csv(self.scopedir+'water_sand.csv',encoding='utf-8',index=False)
        
    def fix_html_title(self,cas):
        # also adds favicon to browser tab
        with open(self.jupyter_fn,'r',encoding='utf-8') as f:
            alltext = f.read()
        alltext  = alltext.replace('<title>chemical_report</title>',
                                   f'<title>{cas}: Open-FF report</title>\n<link rel="icon" href="https://storage.googleapis.com/open-ff-common/favicon.ico">',1)
        with open(self.jupyter_fn,'w',encoding='utf-8') as f:
            f.write(alltext)
            
    def add_favicon(self,fn):
        # also adds favicon to browser tab
        with open(fn,'r',encoding='utf-8') as f:
            alltext = f.read()
        alltext  = alltext.replace('</title>',
                                   '</title>\n<link rel="icon" href="https://storage.googleapis.com/open-ff-common/favicon.ico">',1)
        with open(fn,'w',encoding='utf-8') as f:
            f.write(alltext)

    def make_10perc_dict(self,fromScratch=True):
        if fromScratch:
            self.perc90dic = {}
            caslist = self.allrec.bgCAS.unique().tolist()
            for cas in caslist:
                print(cas)
                df = self.allrec[self.allrec.bgCAS==cas][['bgCAS','bgMass']]
                try:
                    perc90_mass = np.percentile(df[df.bgMass>0].bgMass,90)
                except:
                    perc90_mass = '???'
                self.perc90dic[cas] = perc90_mass
            with open('perc90dic.pkl','wb') as f:
                pickle.dump(self.perc90dic,f)
        else:
            with open('perc90dic.pkl','rb') as f:
                self.perc90dic = pickle.load(f)

    def make_robot_file(self):
        """create robots.txt file"""
        s = "User-agent: * \n"
        s+= "Disallow: / \n"
        self.save_page(webtxt=s,fn='robots.txt')

    def make_jupyter_output(self,subfn=''):
        s= 'jupyter nbconvert --no-input --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --execute work/chemical_report.ipynb --to=html '
        subprocess.run(s)

    def gen_index_page(self,fn):
        name = fn[:-6]
        print(f'*** creating index from {fn}')
        s= f'jupyter nbconvert --no-input --ExecutePreprocessor.allow_errors=True --ExecutePreprocessor.timeout=-1 --execute {fn} --to=html '
        subprocess.run(s)
        self.add_favicon(name+'.html')
        try:
            shutil.move(name+'.html',self.outdir+name+'.html')
        except:
            print(f'Couldnt move {name} result to {self.outdir}')

    def make_new_index_pages(self):
        lst = ['Open-FF_Catalog.ipynb','Open-FF_Chemicals.ipynb',
               'Open-FF_Synonyms.ipynb','Open-FF_Companies.ipynb',
               'Open-FF_TradeNames.ipynb','Open-FF_CASNumber_and_IngredientName.ipynb',
               'Open-FF_Data_Dictionary.ipynb','Open-FF_Conflicting_Chemical_IDs.ipynb',
               'Open-FF_Scope_and_Aggregate_Stats.ipynb']
        #lst = ['Open-FF_Chemicals.ipynb','Open-FF_Data_Dictionary.ipynb']
        for fn in lst:
            self.gen_index_page(fn)
            
            
