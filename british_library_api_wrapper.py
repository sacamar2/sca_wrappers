from funcs_bl_api_wrapper import *
from variables_bl_api_wrapper import *

def image_book_composer():
    all_raw_metadata_each_canvas=get_all_raw_metadata_each_canvas()
    canvases_url=build_canvases_url(all_raw_metadata_each_canvas)
    do_download_all_canvas(canvases_url)
    do_merge_all_canvas()

def metadata_extractor():
    #first_page_html,searches_url=build_searches_urls(['davis', 'harrison'])
    searches_urls=build_searches_urls(['davis', 'harrison'])
    all_books_metadata_urls=build_all_books_metadata_urls(searches_urls)
    all_book_metadatas=get_all_book_metadatas(all_books_metadata_urls)
    full_book_metadata=build_full_book_metadata(all_book_metadatas)
    return full_book_metadata
    