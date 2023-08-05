# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 15:12:41 2023

@author: garya

This code builds a full set of redirect HTML files to use when moving the
whole catalog to a new server.  All HTML files in the ref_dir will be used
to create the new redirect site.


"""

import os
ref_dir = r"C:\MyDocs\OpenFF\src\openFF-catalog\out\cloud_repo"
out_dir = './out/redirect'
new_home = 'https://storage.googleapis.com/open-ff-browser'

def make_HTML(url):
    return f"""<!DOCTYPE html>
<html>
  <head>
    <meta http-equiv="refresh" content="3; url={url}" />
  </head>
  <body>
    <p><h2>You are being redirected to the new home of this page at Open-FF!</h2><br>
    {url}<br> You will be there in a few seconds...</p>
  </body>
</html>"""

def store_redir():
    pass

def process_dir(root,stem):
    dlst = os.listdir(os.path.join(root,stem))
    for item in dlst:
        PATH = os.path.join(root,stem,item)
        if os.path.isdir(PATH):
            try:
                os.mkdir(os.path.join(out_dir,stem,item))
            except:
                pass
            process_dir(root,os.path.join(stem,item))
        else:
            if os.path.isfile(PATH):
                if PATH[-5:] == '.html':
                    branch = os.path.join(new_home,stem,item)
                    html = make_HTML(branch)
                    #print(html)
                    with open(os.path.join(out_dir,stem,item),'w') as f:
                        f.write(html)
                    
                    

if __name__ == '__main__':
    try:
        os.mkdir(out_dir)
    except:
        pass
    process_dir(root=ref_dir,stem='')
