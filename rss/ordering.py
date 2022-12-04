from bs4 import BeautifulSoup as bs
from proxy import rssNews
import requests as r
import random
import time


rsss_view = [
    'https://www.farsnews.ir/rss/mostvisitednews',
    'https://kayhan.ir/fa/rss/all/mostvisited',
    'https://www.entekhab.ir/fa/rss/all/mostvisited',
    r'https://www.tasnimnews.com/fa/rss/feed/0/7/0/%D9%BE%D8%B1%D8%A8%DB%8C%D9%86%D9%86%D8%AF%D9%87-%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1?hit=1', #پربیننده‌ترین اخبار
    'https://www.mehrnews.com/rss/pl/11', #پربازدیدترین

]
rsss_important = [
    'https://www.irna.ir/rss-homepage',

    'https://www.farsnews.ir/rss/topnews',
    # 'https://www.farsnews.ir/rss/chosennews',

    r'https://www.tasnimnews.com/fa/rss/feed/0/8/0/%D9%85%D9%87%D9%85%D8%AA%D8%B1%DB%8C%D9%86-%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1', #مهمترین اخبار
    # r'https://www.tasnimnews.com/fa/rss/feed/0/9/0/%D8%A7%D8%AE%D8%A8%D8%A7%D8%B1-%D8%A8%D8%B1%DA%AF%D8%B2%DB%8C%D8%AF%D9%87', #اخبار برگزیده

    'https://www.mehrnews.com/rss-homepage',
    # 'https://www.mehrnews.com/rss/pl/9', #۱۰ خبر اول
    # 'https://www.mehrnews.com/rss/pl/1', #تیتریک صفحه اول
    # 'https://www.mehrnews.com/rss/pl/2', #تیتردو صفحه اول

    'https://www.khabaronline.ir/rss-homepage',
    # 'https://www.khabaronline.ir/rss/pl/265', #انتخاب سردبیر

    'https://www.isna.ir/rss-homepage',
    # 'https://www.isna.ir/rss/pl/269', #تاپ یک باشگاه
    # 'https://www.isna.ir/rss/pl/260', #تاپ یک صفحه اصلی
    # 'https://www.isna.ir/rss/pl/2', #تاپ دو صفحه اول

    'https://www.entekhab.ir/fa/rss/1', #صفحه نخست

    'https://www.zoomit.ir/feed' #دسته بندی نداشت
]


# MABNA : sleep_time_for_every_web_site_content_request_get
def order(   sleep_time_for_every_web_site_content_request_get=1
            , sleep_time_for_processing_every_single_news=1
            , sleep_time_for_each_time_crawling_the_newses_web_sites=900 ): # 900-seconds = 15-minutes
    try:
        #---######################### rsss_important #########################---#


        news = []
        for rss in rsss_important:
            try:
                text = r.get(rss).text
            except:
                continue
            time.sleep(sleep_time_for_every_web_site_content_request_get) # second(s) Sleep for every web-site-content request.get
            bsd = bs(text)
            items = bsd.find_all('item')


            news.extend([rss, i] for i in items)

        # MAKE A SHUFFLE LIST
        random.shuffle(news)


        for n in news:
            if n[1].link and n[1].link.text.strip()!='':
                guid = n[1].link.text.strip()
            if n[1].guid and n[1].guid.text.strip()!='':
                guid = n[1].guid.text.strip()
            if n[1].link and n[1].link.text.strip()=='':
                link = n[1].link
                guid = link.next.strip()


            # Error Check
            if (guid is None) or (len(guid) <= 0):
                continue


            try:
                get_news = rssNews.objects.filter(guid__icontains=guid).order_by('-id').first()
            except Exception as e:
                print(e)
                get_news = None

            if get_news and (get_news.is_important == False):
                get_news.is_important = True
                get_news.save()

                print('Is-important')


            if sleep_time_for_every_web_site_content_request_get > 0:
                time.sleep(sleep_time_for_processing_every_single_news) # (1)-second(s) For Every Single NEWS Processing # this is because the system and cpu do not being too busy

            guid = None


        #---######################### rsss_view #########################---#


        news = []
        for rss in rsss_view:
            try:
                text = r.get(rss).text
            except:
                continue
            time.sleep(sleep_time_for_every_web_site_content_request_get) # second(s) Sleep for every web-site-content request.get
            bsd = bs(text)
            items = bsd.find_all('item')


            news.extend([rss, i] for i in items)

        # MAKE A SHUFFLE LIST
        random.shuffle(news)


        for n in news:
            if n[1].link and n[1].link.text.strip()!='':
                guid = n[1].link.text.strip()
            if n[1].guid and n[1].guid.text.strip()!='':
                guid = n[1].guid.text.strip()
            if n[1].link and n[1].link.text.strip()=='':
                link = n[1].link
                guid = link.next.strip()


            # Error Check
            if (guid is None) or (len(guid) <= 0):
                continue


            try:
                get_news = rssNews.objects.filter(guid__icontains=guid).order_by('-id').first()
            except Exception as e:
                print(e)
                get_news = None

            if get_news and (get_news.check == False):
                get_news.view += 1
                get_news.check = True
                get_news.save()

                print('View++')

            if sleep_time_for_every_web_site_content_request_get > 0:
                time.sleep(sleep_time_for_processing_every_single_news) # (1)-second(s) For Every Single NEWS Processing # this is because the system and cpu do not being too busy

            guid = None


        if sleep_time_for_every_web_site_content_request_get > 0:
            time.sleep(sleep_time_for_each_time_crawling_the_newses_web_sites) # (900-seconds/15-minutes)-second(s) For each time crawling the NEWSes web-sites

    except Exception as e:
        print(e)