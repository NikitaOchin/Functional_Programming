import asyncio
from concurrent.futures import Future
from typing import Union, Any, Coroutine

import aiohttp
import reactivex
from reactivex import Observable
from reactivex import create
from reactivex.abc import ObserverBase
from reactivex import operators as ops
from reactivex.disposable import Disposable
from reactivex.scheduler.eventloop import AsyncIOScheduler

from bs4 import BeautifulSoup
from pyppeteer import launch

YahooNewsURL = 'https://finance.yahoo.com/quote/AAPL'


async def fetch_data():
    browser = await launch(executablePath="C:\Program Files (x86)\Google\Chrome\Application\chrome.exe", headless=True)
    page = await browser.newPage()
    await page.goto(YahooNewsURL, waitUntil='networkidle0')
    await page.waitForSelector('#tabpanel-news')
    html = await page.content()
    await browser.close()
    try:
        soup = BeautifulSoup(html, 'html.parser')
    except Exception:
        return Exception
    return (soup, 'AAPL')


def connect(subscription_loop: asyncio.AbstractEventLoop) -> Observable[Any]:
    def on_subscribe(observer: ObserverBase[str], scheduler):
        task = asyncio.run_coroutine_threadsafe(fetch_data(), loop=subscription_loop)

        def handle_result(result):
            observer.on_next(result.result())
            observer.on_completed()
            observer.on_error(result)

        task.add_done_callback(handle_result)

        return Disposable(lambda: task.cancel())  # type: ignore

    return create(on_subscribe)


async def await_and_cancel():
    disposable = connect(asyncio.get_running_loop()).subscribe(on_next=print)
    await asyncio.sleep(5000)
    # print("cancelling task")

    # disposable.dispose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    loop.create_task(await_and_cancel())

    loop.run_forever()
