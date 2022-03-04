#!/usr/bin/env python3

import argparse
import csv
import datetime
import logging
import os
import requests
import sys

from multiprocessing import Pool
from pathlib import Path

try:
    assert sys.stdout.isatty()
    from termcolor import colored
except (AssertionError, ImportError):

    def colored(text, *args, **kwargs):
        """Dummy function to pass text through without escape codes if stdout is not a
        TTY or termcolor is not available."""
        return text


URLS_PATH = Path("urls.txt")
OUTPUT_PATH = Path("data.csv")


def check(url):
    logging.debug("Checking %s", url)
    try:
        _response = requests.get(url, timeout=30)
        logging.info(colored("ok %s", "green"), url)
        return
    except Exception as e:
        logging.info(colored("error: %s", "red"), url)
        return {
            "time": datetime.datetime.now().isoformat(),
            "url": url,
            "error": str(e),
        }


def check_urls(urls, output_stream):
    # time that the run started
    started = datetime.datetime.now().isoformat()

    # start up processes to check the URLs
    with Pool(len(os.sched_getaffinity(0))) as pool:
        logging.info(colored("%s checking %d urls", "yellow"), started, len(urls))
        for result in pool.map(check, urls):
            if result:
                result["run"] = started
                output_stream.writerow({"run": started, **result})


def main():

    parser = argparse.ArgumentParser(description="Description: {}".format(__file__))

    parser.add_argument(
        "-v", "--verbose", action="store_true", default=False, help="Increase verbosity"
    )
    parser.add_argument(
        "-q", "--quiet", action="store_true", default=False, help="Quiet operation"
    )

    args = parser.parse_args()

    log_level = logging.DEBUG if args.verbose else logging.INFO
    log_level = logging.CRITICAL if args.quiet else log_level
    logging.basicConfig(level=log_level, format="%(message)s")

    with URLS_PATH.open("r", encoding="utf8") as _fh:
        urls = [_.strip() for _ in _fh.readlines()]

    with OUTPUT_PATH.open("a", encoding="utf8") as _fh:
        writer = csv.DictWriter(_fh, fieldnames=["run", "time", "url", "error"])
        if not _fh.tell():
            writer.writeheader()
        check_urls(urls, writer)


if __name__ == "__main__":
    main()
