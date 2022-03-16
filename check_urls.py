#!/usr/bin/env python3

import argparse
import asyncio
import csv
import datetime
import logging
import sys
from socket import gethostbyname

from pathlib import Path

import aiohttp


try:
    assert sys.stdout.isatty()
    from termcolor import colored
except (AssertionError, ImportError):

    def colored(text, *args, **kwargs):
        """Dummy function to pass text through without escape codes if stdout is not a
        TTY or termcolor is not available."""
        return text


URLS_PATH = Path("urls.txt")

async def check_url(session, url, i):
    logging.debug(colored("Checking %s", "yellow"), url)
    try:
        async with session.get(url) as _:
            logging.info(colored("%s : ok: %s", "green"), f"{i: >5}", url)
            return
    except Exception as e:
        logging.info(colored("%s : error: %s", "red"), f"{i: >5}", url)
        return {
            "time": datetime.datetime.now().isoformat(),
            "url": url,
            "error": str(e),
        }


async def check_urls(urls, output_stream):
    started = datetime.datetime.now().isoformat()

    connector = aiohttp.TCPConnector(limit=50)

    async with aiohttp.ClientSession(connector=connector) as session:
        tasks = []
        for i, url in enumerate(urls):
            tasks.append(asyncio.ensure_future(check_url(session, url, i)))
            await asyncio.sleep(0.5)

        rows = await asyncio.gather(*tasks)

    for row in (_ for _ in rows if _ is not None):
        output_stream.writerow({"run": started, **row})


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
        loop = asyncio.get_event_loop()
        loop.run_until_complete(check_urls(urls, writer))


if __name__ == "__main__":
    main()
