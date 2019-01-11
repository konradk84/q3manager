def set_info_query(base):
    info = base
    info += b'getinfo xxx'
    return info
def set_status_query(base):
    status = base
    status += b'getstatus xxx'
    return status