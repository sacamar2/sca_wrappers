import pandas as pd
import numpy as np
import requests
import json
from time import sleep
from PIL import Image
from glob import glob
import re
import os
import itertools
from bs4 import BeautifulSoup as bs
from funcs_bl_api_wrapper import *
from variables_bl_api_wrapper import *

# BOOK COMPOSER FROM IMAGES
def get_all_raw_metadata_each_canvas():
    a=s.get(f'{base_url_metadata}.0x000001/manifest.json')
    all_raw_metadata_each_canvas=json.loads(a.content)
    return all_raw_metadata_each_canvas

def build_canvases_urls(all_raw_metadata_each_canvas):
    if all_pages:
        canvases_url=all_raw_metadata_each_canvas['structures'][-1]['canvases']
        canvases_id=["{0:#0{1}x}".format(i,8) for i in range(1,len(canvases_url)+1)]
        
    elif page_range and not(all_pages):
        canvases_url=all_raw_metadata_each_canvas['structures'][-1]['canvases']
        canvases_id=["{0:#0{1}x}".format(i,8) for i in range(start_page,end_page+1)]    
    
    elif not(page_range) and not(all_pages):
        canvases_url=all_raw_metadata_each_canvas['structures'][-1]['canvases']
        canvases_id=["{0:#0{1}x}".format(i,8) for i in specific_pages]
    
    canvases_url=[f'{base_url_metadata}.{id}/full/max/0/default.jpg' for id in canvases_id]
    return canvases_url

def do_download_all_canvas(canvases_url):
    counter=0
    for canvas in canvases_url:
        counter+=1
        str_canvas_img=s.get(canvas).content
        file = open(fr"{canvases_output_folder}/page_{counter}.png", "wb")
        file.write(str_canvas_img)
        file.close()
        if counter%25==0:
            sleep(sleep_time)

def do_merge_all_canvas():
    list_images=glob("*.png")
    list_images.sort(key=os.path.getmtime)
    
    images=[Image.open(f) for f in list_images]
    images[0].save(book_output_filename,resolution=resolution_dpi, save_all=True,append_images=images[1:])

    
def main_image_book_composer():
    all_raw_metadata_each_canvas=get_all_raw_metadata_each_canvas()
    canvases_url=build_canvases_url(all_raw_metadata_each_canvas)
    do_download_all_canvas(canvases_url)
    do_merge_all_canvas()


# METADATA EXTRACTOR

## Build the list of all the urls where the metadata of the books is
def build_searches_urls(searches_keywords):
    ''' This method contains the pattern used for all the search pages in order to extract from them the metadata book webpage url '''
    print('We start to get all the searches pages')
    searches_keywords_joined='+'.join(searches_keywords)
    first_page=do_bl_req(f"{base_url_book_searches}&indx=1&vl(freeText0)={searches_keywords_joined}")
    first_page_html=bs(first_page.content)
    ts=first_page_html.find_all('table')
    ems=first_page_html.find_all('em')[0]
    search_result_len=int(re.sub("[^0-9]","",ems.getText()))
    
    total_pages=round((search_result_len-10)/10)
    
    searches_urls=[]
    for tp in range(0,total_pages-1):
        aux_search_urls=f"{base_url_book_searches}&pag=nxt&indx={tp*10+1}&vl(freeText0)={searches_keywords_joined}"
        searches_urls.append(aux_search_urls)
    
    #return first_page_html,searches_urls
    return searches_urls

def get_page_books_metadata_urls(page_html):
    ''' This method get all the urls of the metadata webpage of each book on a search page '''
    raw_page_books_metadata_urls=page_html.find_all('h2',{'class':'EXLResultTitle'})
    
    page_books_metadata_urls=[]
    for m in raw_page_books_metadata_urls:
        m_cleaned=re.sub(r';.+\?', '?',m.a['href'].replace('moreTab','detailsTab'))
        page_books_metadata_urls.append(f"{base_url_book_metadata}/{m_cleaned}")
    
    return page_books_metadata_urls

def build_all_books_metadata_urls(searches_urls):
    ''' This method build a table with all the metadata urls of the whole search'''
    all_books_metadata_urls=[]
    for s_url in searches_urls:
        page_html=bs(do_bl_req(s_url).content)
        page_books_metadata_urls=get_page_books_metadata_urls(page_html)
        all_books_metadata_urls.append(page_books_metadata_urls)
    
    all_books_metadata_urls=list(itertools.chain(*all_books_metadata_urls))
    #clean_data=pd.DataFrame(columns=['author','energy','time'])
    #config_multi_pool=list(itertools.product(np.unique(input_data['node_type']),range(max_time_steps),[input_data]))
    #print('multi starting')
    #
    #with multiprocessing.Pool() as pool:
    #    raw_results=zip(*pool.map(processData.build_clean_per_time_point,config_multi_pool))
    #
    #pool.close()
    #pool.join()
    #
    #raw_clean_data=list(raw_results)[0]
    #for r in raw_clean_data:
    #    aux_clean_data=pd.DataFrame({'node_type':[r[0]],'energy':[r[1]],'time':[r[2]]})
    #    clean_data=clean_data.append(aux_clean_data)
    
    return all_books_metadata_urls

def get_book_metadata(book_url):
    b_data=do_bl_req(book_url)
    b_data_html=bs(b_data.content)
    raw_book_metadata=b_data_html.find('div',{'class':'EXLDetailsContent'}).find('ul').find_all('li')
    book_metadata=[]
    for d in raw_book_metadata:
        try:
            aux_book_metadata=[d['id'].replace('-1',''),d.span.text]
            book_metadata.append(aux_book_metadata)
        except:
            try:
                aux_book_metadata=[d['id'].replace('-1',''),d.a.text]
                book_metadata.append(aux_book_metadata)
            except:
                try:
                    aux_book_metadata=[d['id'].replace('-1',''),d.div.text]
                    book_metadata.append(aux_book_metadata)
                except:
                    try:
                        aux_book_metadata=[d.text.split(":")[0].replace("\n","").replace("\t",""),d.text.split(":")[1].replace("\n","").replace("\t","")]
                        book_metadata.append(aux_book_metadata)
                    except:
                        continue
                    continue
                continue
            
            continue
    return book_metadata

def get_all_book_metadatas(all_books_metadata_urls):
    all_book_metadatas=[]
    for bmu in all_books_metadata_urls:
        aux_all_book_metadatas=get_book_metadata(bmu)+[['webpage',bmu]]
        all_book_metadatas.append(aux_all_book_metadatas)
    
    return all_book_metadatas

def build_full_book_metadata(all_book_metadatas):
    raw_metadata_columns=[list(dict(m).keys()) for m in all_book_metadatas]
    metadata_columns=np.unique(list(itertools.chain(*raw_metadata_columns)))
    metadata_values=[dict(m) for m in all_book_metadatas]
    full_book_metadata=pd.DataFrame(columns=metadata_columns,data=metadata_values)
    return full_book_metadata

def do_bl_req(url):
    KO=True
    while KO:
        try:
            bl_req=requests.get(url)
        except:
            print('There were some issue trying to get the data.')
            continue
        if bl_req.status_code==200:
            KO=False
            print(f'We got a {bl_req.status_code}, so we can continue.')
            return bl_req
        else:
            print('We have been blocked, we try again')
            sleep(11)

def main_metadata_extractor():
    #first_page_html,searches_url=build_searches_urls(['davis', 'harrison'])
    searches_urls=build_searches_urls(['davis', 'harrison'])
    all_books_metadata_urls=build_all_books_metadata_urls(searches_urls)
    all_book_metadatas=get_all_book_metadatas(all_books_metadata_urls)
    full_book_metadata=build_full_book_metadata(all_book_metadatas)
    return full_book_metadata

# FULL IMAGES EXTRACTOR





