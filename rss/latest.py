from proxy import Category, rssNews
from bs4 import BeautifulSoup as bs
import requests as r
import random
import time
import re


rsss = [
    ['تسنیم', 'https://www.tasnimnews.com', 'https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D8%A2%D8%AE%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%B1%D9%88%D8%B2',],
    ['فارس', 'https://www.farsnews.ir', 'https://www.farsnews.ir/rss',],
    ['مهر', 'https://www.mehrnews.com', 'https://www.mehrnews.com/rss',],
    ['ایرنا', 'https://www.irna.ir', 'https://www.irna.ir/rss',],
    ['ایسنا', 'https://www.isna.ir', 'https://www.isna.ir/rss',],
    ['ایلنا', 'https://www.ilna.news', 'https://www.ilna.news/feeds',],
    ['کیهان', 'https://www.kayhan.ir', 'https://www.kayhan.ir/fa/rss/allnews',],
    ['انتخاب', 'https://www.entekhab.ir', 'https://www.entekhab.ir/fa/rss/allnews',],
    ['خبر آنلاین', 'https://www.khabaronline.ir', 'https://www.khabaronline.ir/rss',],
    ['زومیت', 'https://www.zoomit.ir', 'https://www.zoomit.ir/feed',],
]


# MABNA : sleep_time_for_every_web_site_content_request_get
def latest(   sleep_time_for_every_web_site_content_request_get=1
            , sleep_time_for_processing_every_single_news=1
            , sleep_time_for_each_time_crawling_the_newses_web_sites=900 ): # 900-seconds = 15-minutes
    
    try:
        news = []
        for rss in rsss:
            text = r.get(rss[2]).text
            time.sleep(sleep_time_for_every_web_site_content_request_get) # second(s) Sleep for every web-site-content request.get
            bsd = bs(text, 'html.parser')
            items = bsd.find_all('item')

            news.extend([rss, i] for i in items)

        # MAKE A SHUFFLE LIST
        random.shuffle(news)


        for n in news:
            description = None
            category = None
            media = None
            guid = None
            title = None


            if n[1].description and n[1].description.text.strip()!='':
                description = n[1].description.text.strip()
                description = re.sub(r'&.{1,6};', '', description)
                description = re.sub(r'<img.*">', '', description)
                description = re.sub(r'<img.* ">', '', description)
                description = re.sub(r'<img.*"/>', '', description)
                description = re.sub(r'<img.*" />', '', description)
                description = re.sub(r'<.*/>', '', description)
                description = re.sub(r'<.* />', '', description)
                description = re.sub(r'<[a-z]+>', '', description)
                description = re.sub(r'</.*>', '', description)
                description = description.replace('&amp;', '') \
                                            .replace('&nbsp;','') \
                                            .replace('nbsp;','') \
                                            .replace('&', '') \
                                            .replace('  ', ' ') \
                                            .replace('<![CDATA[', '') \
                                            .replace(']]>', '') \
                                            .strip()

            if n[1].category and n[1].category.text.strip()!='':
                category = n[1].category.text.replace('/', '|') \
                                            .strip()

            if n[1].media and n[1].media.get('url').strip()!='':
                media = n[1].media.get('url').strip()
            if n[1].thumbnail and n[1].thumbnail.get('url').strip()!='':
                media = n[1].thumbnail.get('url').strip()
            if n[1].enclosure and n[1].enclosure.get('url').strip()!='':
                media = n[1].enclosure.get('url').strip()

            if n[1].title and n[1].title.text.strip()!='':
                title = n[1].title.text.strip()
                title = re.sub(r'&.{1,6};', '', title)
                title = re.sub(r'<img.*">', '', title)
                title = re.sub(r'<img.* ">', '', title)
                title = re.sub(r'<img.*"/>', '', title)
                title = re.sub(r'<img.*" />', '', title)
                title = re.sub(r'<.*/>', '', title)
                title = re.sub(r'<.* />', '', title)
                title = re.sub(r'<[a-z]+>', '', title)
                title = re.sub(r'</.*>', '', title)
                title = title.replace('&', '') \
                            .replace('  ', ' ') \
                            .replace('/', '،') \
                            .replace('«', '"') \
                            .replace('»', '"') \
                            .strip()

            if n[1].link and n[1].link.text.strip()!='':
                guid = n[1].link.text.strip()
            if n[1].guid and n[1].guid.text.strip()!='':
                guid = n[1].guid.text.strip()
            if n[1].link and n[1].link.text.strip()=='':
                link = n[1].link
                guid = link.next.strip()


            # Error Check
            if ( (title is None) or (len(title) <= 0) ) or ( (guid is None) or (len(guid) <= 0) ):
                continue


            if category:
                category, is_category_created = Category.objects.get_or_create(title=category[:128] if category is not None else None)


            try:
                rssNews.objects.get_or_create(news_publisher_name=n[0][0][:128] if n[0][0] is not None else None, news_publisher_address=n[0][1][:2048] if n[0][1] is not None else None, description=description[:4096] if description is not None else None, category=category, media=media[:2048] if media is not None else None, guid=guid[:2048] if guid is not None else None, title=title[:128] if title is not None else None)

                print('created')
            except Exception as e:
                print(e)
            if sleep_time_for_every_web_site_content_request_get > 0:
                time.sleep(sleep_time_for_processing_every_single_news) # (1)-second(s) For Every Single NEWS Processing # this is because the system and cpu do not being too busy

        if sleep_time_for_every_web_site_content_request_get > 0:
            time.sleep(sleep_time_for_each_time_crawling_the_newses_web_sites) # (900-seconds/15-minutes)-second(s) For each time crawling the NEWSes web-sites

    except Exception as e:
        print(e)