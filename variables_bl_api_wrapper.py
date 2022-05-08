import os
import requests
s=requests.Session()

ark_id='81055'
vdc_id='vdc_100064129070'
base_url_metadata=f'https://api.bl.uk/metadata/iiif/ark:/{ark_id}/{vdc_id}'

base_url_book_searches='http://explore.bl.uk/primo_library/libweb/action/search.do?fctN=facet_rtype&fctV=books&fn=search&'
base_url_book_metadata='http://explore.bl.uk/primo_library/libweb/action'

resolution_dpi=300
book_output_filename='book.pdf'

canvases_output_folder='.'

all_pages=True
page_range=True

start_page=1
end_page=-1

specific_pages=[1,10]

sleep_time=10 # In order to avoid blocker of the IP because of too many requests. It is in seconds, we reccommend 10 secs.


