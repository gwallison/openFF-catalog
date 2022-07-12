# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:00:34 2020

@author: Gary

This code is used to direct the process of making a static web site of
a chemical catelog.
"""

from catalog_common import repo_name, bulkdata_date
import work.gen_chemical_catalog as gen_cat

mode = 'test'
mode = 'main'

outdir = r"E:\working\catalog\website_Jun30_2022/"

if mode=='test':
    wg = gen_cat.Web_gen(repo_name=repo_name,
                          data_date=bulkdata_date,
                           outdir = outdir,
                           # caslist=['50-00-0','7732-18-5',
                           #            '111-76-2','100-52-7',
                           #            '10028-15-6',
                           #            '814-80-2',
                           #            '71-43-2','8008-20-6',
                           #            '9002-84-0','108-95-2',
                           #            '79-06-1','7727-37-9',
                           #           '111560-38-4',
                           #           '100-44-7','100-79-8',
                           #           'proprietary'])
                          caslist=['50-00-0'])
else:
    wg = gen_cat.Web_gen(repo_name=repo_name,
                         data_date=bulkdata_date,caslist=[],
                         outdir = outdir)

#wg.make_chem_list()
#wg.make_state_set()
#wg.make_scope_data()
wg.make_colab_set()
#wg.make_new_index_pages()
