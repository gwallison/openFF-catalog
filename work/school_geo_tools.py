# -*- coding: utf-8 -*-
"""
Created on Fri Nov  4 21:06:35 2022

@author: Gary
"""
import sys
sys.path.insert(0,'c:/MyDocs/OpenFF/src/')
from common.code import Analysis_set_remote as ana_set
work_pickles = 'c:/MyDocs/OpenFF/src/common/'

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
final_crs = 4326 # WGS84
proj_crs = 3857 # convert to this when calculating distances
def_buffer = 1609.34 # one mile



# shapefile names
district_fn = r"C:\MyDocs\OpenFF\data\external_refs\shape_files\schools\School_District_Composites_SY_2020-21_TL_21.zip"

def get_FFdf_as_gdf():
    # df = ana_set.Full_location(repo = 'v15_beta_2022_11_02_min',
    df = ana_set.Full_location(repo = 'cloud_repo_2023_04_27',
                     force_new_creation=False,
                     outdir=work_pickles).get_set()
    gb = df.groupby('api10',as_index=False)[['bgLatitude',
                                             'bgLongitude',
                                             'bgStateName']].first()
    gdf =  gpd.GeoDataFrame(gb, geometry= gpd.points_from_xy(gb.bgLongitude, 
                                                             gb.bgLatitude,
                                                             crs=final_crs))
    return gdf
    
def get_all_wells_as_gdf():
    df = pd.read_csv(r"C:\MyDocs\OpenFF\data\external_refs\state_latlon.csv",
                              dtype={'api10':str},low_memory=False,
                              quotechar='$',encoding='utf-8')

    gb = df.groupby('api10',as_index=False)[['stLatitude',
                                             'stLongitude']].first()
    gb['bgStateNumber'] = gb.api10.str[:2]
    api = pd.read_csv(r"C:\MyDocs\OpenFF\data\external_refs\API_num_ref.csv",
                      dtype={'bgStateNumber':str})
    gb = pd.merge(gb,api[['bgStateNumber','bgStateName']],on='bgStateNumber',
                  how='left')
    gdf =  gpd.GeoDataFrame(gb[['stLatitude','stLongitude','api10',
                                'bgStateName']], geometry= gpd.points_from_xy(gb.stLongitude, 
                                                             gb.stLatitude,
                                                             crs=final_crs))
    #print(gdf.head())                                                                             
    return gdf

def num_wells_per_district(outfilename='./tmp/FFwells_in_school_districts.csv'):
    wells = get_FFdf_as_gdf()
    schdf = gpd.read_file(district_fn)   
    schdf = schdf.to_crs(final_crs) #reproject
    dfsjoin = gpd.sjoin(schdf,wells)
    dfsjoin = dfsjoin.fillna('--')
    gb = dfsjoin.groupby(['bgStateName','NAME','GEOID'],as_index=False)['api10'].count().rename({'api10':'num_FF_wells'},axis=1)
    
    # Now do the same for all wells from state data
    wells = get_all_wells_as_gdf()
    # print(wells.columns)
    dfsjoin = gpd.sjoin(schdf,wells)
    dfsjoin = dfsjoin.fillna('--')
    gb1 = dfsjoin.groupby(['bgStateName','NAME','GEOID'],as_index=False)['api10'].count().rename({'api10':'num_all_wells'},axis=1)
    
    mg = pd.merge(gb,gb1,on=['bgStateName','NAME','GEOID'],how='outer')
    out = mg.sort_values('num_FF_wells',ascending=False)
    out.to_csv(outfilename)
    # print(out)
    
def find_schools_near_well_set(well_gdf,buffer_m=def_buffer):
    # return a df with all schools within bufferrange of point
    return pd.DataFrame()

def find_wells_near_point(lat,lon,wellgdf,crs=final_crs,name='test',
                          buffer_m=def_buffer, bbnum=0.25):
    # use bounding box to shrink number of wells to check
    t = wellgdf.cx[lon-bbnum:lon+bbnum, lat-bbnum:lat+bbnum]
    t = t.to_crs(proj_crs)
    s = gpd.GeoSeries([Point(lon,lat)],crs=crs)
    s = s.to_crs(proj_crs)
    s = gpd.GeoDataFrame(geometry=s.geometry.buffer(buffer_m))
    s['name'] = name
    tmp = gpd.sjoin(t,s,how='inner',predicate='within')
    return tmp.api10.tolist()

if __name__ == '__main__':
    wells_gdf = get_FFdf_as_gdf()
    lat = wells_gdf.iloc[100000].bgLatitude
    lon = wells_gdf.iloc[100000].bgLongitude
    print(find_wells_near_point(lat,lon,wells_gdf))
    #num_wells_per_district()
