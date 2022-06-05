from latest import latest
from ordering import order
from seed import seed


fast = True # True is for testing, False is for production

# "seed" works with "sleep_time_for_every_web_site_content_request_get" of "0" for the "lates" function inside of it that means it works in "fast" mode(testing mode)
seed()

while(True):
    """
    This is the main loop of the program.

    The functions(latest and order) time working [their arguments is in second(s)]:
        sleep_time_for_every_web_site_content_request_get=1 # This is the main parameter that controls the two other parameters below (turns them off) when it is "0" AND when it is "0" the App goes in fast mode(testing mode)
        sleep_time_for_processing_every_single_news=1
        sleep_time_for_each_time_crawling_the_newses_web_sites=900 / 15-minutes
    """
    
    if fast:
        order(sleep_time_for_every_web_site_content_request_get=0)
        latest(sleep_time_for_every_web_site_content_request_get=0)
    else: # means normal mode
        latest()
        order()
