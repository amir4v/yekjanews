from proxy import rssNews
from latest import latest


def seed():
    latest(sleep_time_for_every_web_site_content_request_get=0)

    for n in rssNews.objects.order_by('-id')[:20]:
        print(n.id)
        n.is_important = True
        n.save()
