from bs4 import BeautifulSoup as bs
from proxy import AparatVideo
import requests as r
import time


def aparat(t=1): # t is minute(s)
    try:
        text_base = r.get('https://www.aparat.com/political').text
        bs_base = bs(text_base, 'html.parser')

        flag = True
        for a in bs_base.find_all('section', {'class':'list-content'})[0].find_all('a')[::-1]:
            if a.get('href')[:9].startswith('/v/') and flag:
                key = a.get('href')[3:9]
                print(key)

                text_in = r.get(f'https://www.aparat.com/video/video/embed_box/videohash/{key}').text
                bs_in = bs(text_in, 'html.parser')

                div = str(bs_in.find_all('textarea')[1].find_all('div')[0])
                AparatVideo.objects.get_or_create(media=div)

            flag = not flag
        
        time.sleep( 60 * t )
    except Exception as e:
        print(e)
        pass