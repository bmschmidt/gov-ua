#!/usr/bin/env python3

import csv
import time
import pathlib
import datetime
import requests
import multiprocessing
import pandas as pd
import random
import sys

from colorama import init
from termcolor import colored
from pathlib import Path

# collect data every 30 mins
sleep_secs = 60 * 30

def main(fin): # Aarg, an arg for main!
    init()
    urls = open(fin).read().splitlines()
    random.shuffle(urls)    
    # time that the run started
    started = datetime.datetime.now()
    rows = []
    # start up 50 processes to check the URLs
    with multiprocessing.Pool(50) as pool:
        print(colored(f"{started} checking {len(urls)} urls", "yellow"))
        for result in pool.map(check, urls):
            if result:
                result["run"] = started.isoformat()
                rows.append(result)
    print( pd.DataFrame(rows))
    pd.DataFrame(rows).to_parquet(Path("parquet", str(started) + ".parquet"))

    # make sure csv is up to date after each run
#        fh.flush()

#       # sleep for a bit based on how long the run took
#      elapsed = datetime.datetime.now() - started
#     if elapsed.total_seconds() < sleep_secs:
#        t = sleep_secs - elapsed.total_seconds()
 #       print(colored(f"sleeping {t} seconds", "yellow"))
  #      time.sleep(t)

def check(url):
    try:
        with requests.get(url, timeout=30, stream = True) as r:
            ip = r.raw._original_response.fp.raw._sock.getpeername()[0]        
            print(colored(f"ok {url}", "green"))
            return {
                "time": datetime.datetime.now().isoformat(),
                "url": url,
                "ip": ip,
                "status": r.status_code
            }
    except Exception as e:
        print(colored(f"error: {url}", "red"))
        return {
            "time": datetime.datetime.now().isoformat(),
            "url": url,
            "error": str(e)
        }

if __name__ == "__main__":
    try:
        fin = Path(sys.argv[1])
    except IndexError:
        print("Must pass in a file with a list of urls")
        exit()
    main(fin)
