#!/usr/bin/env python
from functools import partial
from multiprocessing import Pool
from socket import socket, setdefaulttimeout, error, gethostbyname
import argparse
import logging


def set_log():
    logger = logging.getLogger()
    logger.setLevel(LOG_LEVEL)

    fm = logging.Formatter('%(filename)s [LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s')

    console = logging.StreamHandler()
    console.setLevel(LOG_LEVEL)
    console.setFormatter(fm)

    logger.addHandler(console)


def ping(host, port):
    try:
        s = socket()
        s.connect((host, port))
        try:
            return port, s.recv(1024)
        except:
            return port, None  # increase the timeout to get more data
    except error:
        if error.errno == 111:  # connection refused
            pass


def multi_processed_scan(host, processes, timeout, lower_border_port, upper_border_port):
    setdefaulttimeout(timeout)
    p = Pool(processes)
    ping_host = partial(ping, host)
    return filter(bool, p.map(ping_host, range(lower_border_port, upper_border_port)))


def parse_args():
    parser = argparse.ArgumentParser(description='Scans all opened ports of specified host')

    parser.add_argument('--host2scan', type=str,
                        help='ip address to scan', default="127.0.0.1")
    parser.add_argument('--processes', '-p', type=int,
                        help='Number of processes', default=200)
    parser.add_argument('--timeout', '-t', type=float,
                        help='Float default timeout used to scan ports', default=.5)
    parser.add_argument('--lower-border-port', '-l', type=int,
                        help='From which port start range scan', default=1)
    parser.add_argument('--upper-border-port', '-u', type=int,
                        help='On which port finish range scan', default=65536)

    return parser.parse_args()


if __name__ == "__main__":
    LOG_LEVEL = 'INFO'  # 'DEBUG'
    set_log()
    config = parse_args()
    host2scan = gethostbyname(config.host2scan)
    logging.info("[+] Scanning host %s processes: %s timeout: %s"
                 " lower_border_port: %s upper_border_port %s ...",
                 host2scan, config.processes, config.timeout,
                 config.lower_border_port, config.upper_border_port)
    opened_ports = list(multi_processed_scan(host2scan, config.processes, config.timeout,
                        config.lower_border_port, config.upper_border_port))
    logging.info(opened_ports)
