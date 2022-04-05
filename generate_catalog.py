# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:00:34 2020

@author: Gary

This code is used to direct the process of making a static web site of
a chemical catelog.
"""

from catalog_common import repo_name, bulkdata_date
import work.gen_chemical_catalog as gen_cat

#mode = 'test'
mode = 'main'

if mode=='test':
    wg = gen_cat.Web_gen(repo_name=repo_name,
                          data_date=bulkdata_date,
                          caslist=['50-00-0',#'7732-18-5',
                                    '111-76-2','100-52-7',
                                    '10028-15-6',
                                    '814-80-2',
                                    '71-43-2',
                                    '9002-84-0',
                                    '79-06-1','7727-37-9',
                                    '100-44-7'])
else:
    wg = gen_cat.Web_gen(repo_name=repo_name,
                         data_date=bulkdata_date,caslist=[])

wg.make_chem_list()
wg.make_scope_data()
wg.make_new_index_pages()
