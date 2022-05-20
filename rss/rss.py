from latest import latest
from ordering import order
from seed import seed


fast = True # True is for testing, False is for production

seed()

while(True):
    if fast:
        latest(sleep_time_for_every_web_site_content_request_get=0)
        order(sleep_time_for_every_web_site_content_request_get=0)
    else: # means normal mode
        latest()
        order()
