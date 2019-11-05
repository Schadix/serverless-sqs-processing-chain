import logging
import os
import json
import requests
from timer.timer import Timer
from collections import defaultdict
import aiohttp
import asyncio
from aiohttp import ClientSession

logger = logging.getLogger(__name__)

test_url = 'https://www.google.com'


def report_progress(timers):
    try:
        r = ["{}: {}\n".format(x, str(timers[x])) for x in timers]
        logger.info('{}'.format("".join(r)))
    except Exception as e:
        logger.error(e)


async def fetch(timers, url, session, request_timeout):
    timers['async-single'].tic()
    async with session.head(url, timeout=request_timeout) as response:
        r = await response.read()
        timers['async-single'].toc()
        return r


async def bound_fetch(timers, sem, url, session, request_timeout):
    # Getter function with semaphore.
    async with sem:
        await fetch(timers=timers, url=url, session=session, request_timeout=request_timeout)


async def run(timers, number_of_requests, request_timeout):
    sem = asyncio.Semaphore(number_of_requests)
    tasks = []
    timers['async-single-bound-fetch'].tic()

    async with ClientSession() as session:
        for i in range(number_of_requests):
            # pass Semaphore and session to every GET request
            task = asyncio.ensure_future(bound_fetch(timers=timers,
                                                     sem=sem,
                                                     url=test_url.format(i),
                                                     session=session,
                                                     request_timeout=request_timeout))
            tasks.append(task)
            timers['async-single-bound-fetch'].toc()

        responses = asyncio.gather(*tasks)
        await responses


def lambda_handler(event, context):
    timers = defaultdict(Timer)
    print(json.dumps(event))
    log_level = os.environ.get('LOG_LEVEL', 'INFO')
    number_of_requests = int(os.environ.get('NR_REQUESTS', '100'))
    request_timeout = float(os.environ.get('REQUEST_TIMEOUT', '5.0'))
    connection_timeout = 0.4
    logger.setLevel(log_level)

    # fire x requests sequentiell
    timers['sequential'].tic()
    for i in range(0, number_of_requests):
        r = requests.get(test_url, timeout=connection_timeout)
        timers['sequential'].toc()

    # fire x requests async
    timers['async-total'].tic()
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(
        run(timers=timers, number_of_requests=number_of_requests, request_timeout=aiohttp.ClientTimeout(request_timeout)))
    loop.run_until_complete(future)
    timers['async-total'].toc()

    report_progress(timers=timers)
