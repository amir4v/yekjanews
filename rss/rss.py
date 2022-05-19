from latest import latest
from ordering import order
from aparat import aparat


fast = True

while(True):
    if fast:
        latest(sleep_time_for_every_web_site_content_request_get=0)
        order(sleep_time_for_every_web_site_content_request_get=0)
        aparat(t=0) # t is minute(s)
    else:
        latest()
        order()
        aparat(t=1) # t is minute(s)
