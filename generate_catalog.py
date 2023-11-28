# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 12:00:34 2020

@author: Gary

This code is used to direct the process of making a static web site of
a chemical catelog.
"""

from catalog_common import repo_name, bulkdata_date, data_source
import work.gen_chemical_catalog as gen_cat

# c = input("If you haven't updated molecular images, abort and do that now.  Continue? (Y/n) > ")
# if c in ['n','N']:
#     exit()

# mode = 'test'
mode = 'main'

# outdir = r"C:\MyDocs\OpenFF\src\openFF-catalog\out\test"
outdir = r"C:\MyDocs\OpenFF\src\openFF-catalog\out\openFF_browser_2023_10_21"
#outdir = r"C:\MyDocs\OpenFF\src\openFF-catalog\out\july30_2022\website_Jul30_2022/"
#outdir = r"C:\MyDocs\OpenFF\src\openFF-catalog\out\website_2023_03_03/"

if mode=='test':
    wg = gen_cat.Web_gen(repo_name=repo_name,
                          data_date=bulkdata_date,
                           outdir = outdir,
                            # caslist=['50-00-0','7732-18-5',
                            #               '111-76-2','100-52-7',
                            #               '488-16-4', '7440-36-0','699-00-3', # not in comptox
                            #               '10028-15-6',
                            #               '814-80-2',
                            #               '71-43-2','8008-20-6',
                            #               '9002-84-0','108-95-2',
                            #               '79-06-1','7727-37-9',
                            #             '111560-38-4','320-31-0',
                            #             '100-44-7','100-79-8',
                            #             'proprietary'],
                           caslist=['proprietary','107-21-1'],
                           data_source=data_source)
else:
    wg = gen_cat.Web_gen(repo_name=repo_name,
                         data_date=bulkdata_date,caslist=[],
                         outdir = outdir,
                         data_source=data_source)

# wg.refresh_external_sets()
wg.make_disclosure_set()
# wg.make_chem_list()
# wg.make_operator_set()
# wg.make_state_set()
# wg.make_scope_data()
# wg.make_new_index_pages()
# wg.save_sitemap()
# wg.make_robot_file()
