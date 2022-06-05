from persiantools.jdatetime import JalaliDateTime


def j_pub_dt():
    jdt = JalaliDateTime.now()
    return (f'{jdt.year}/{jdt.month}/{jdt.day} - {jdt.hour}:{jdt.minute}')
