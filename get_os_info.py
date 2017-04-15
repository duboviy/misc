import os
import time

import psutil           # pip install psutil
import humanfriendly    # pip install humanfriendly


def get_os_info():
    """ Get some OS info with psutils and humanfriendly. """
    is_win = lambda: True if os.name == 'nt' else False
    pid = os.getgid() if not is_win() else None
    ppid = os.getppid()

    now = time.time()

    current_process = psutil.Process(pid=ppid)
    process_uptime = current_process.create_time()
    process_uptime_delta = now - process_uptime
    process_uptime_human = humanfriendly.format_timespan(process_uptime_delta)

    system_uptime = psutil.boot_time()
    system_uptime_delta = now - system_uptime
    system_uptime_human = humanfriendly.format_timespan(system_uptime_delta)

    free_memory = psutil.disk_usage('/').free
    total_memory = psutil.disk_usage('/').total
    percent_used_memory = psutil.disk_usage('/').percent
    used_memory = psutil.disk_usage('/').used
    free_memory_human = humanfriendly.format_size(free_memory)

    return vars()


if __name__ == '__main__':
    from pprint import pprint
    pprint(get_os_info())
    ### Output example:
    # {'current_process': <psutil.Process(pid=10628, name='pycharm.exe') at 2074457600744>,
    #  'free_memory': 28299886592,
    #  'free_memory_human': '28.3 GB',
    #  'is_win': <function get_os_info.<locals>.<lambda> at 0x000001E2FFDED158>,
    #  'now': 1491982808.197413,
    #  'percent_used_memory': 88.2,
    #  'pid': 1001,
    #  'ppid': 10628,
    #  'process_uptime': 1491471889.0,
    #  'process_uptime_delta': 510919.1974129677,
    #  'process_uptime_human': '5 days, 21 hours and 55 minutes',
    #  'system_uptime': 1490198873.0,
    #  'system_uptime_delta': 1783935.1974129677,
    #  'system_uptime_human': '2 weeks, 6 days and 15 hours',
    #  'total_memory': 239530405888,
    #  'used_memory': 211230519296}
