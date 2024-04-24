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

YahooURLAPI = 'https://query1.finance.yahoo.com/v7/finance/chart/AAPL?interval=5m'


async def fetch_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(YahooURLAPI) as resp:
            return await resp.json()


def connect(subscription_loop: asyncio.AbstractEventLoop) -> Observable[Any]:
    def on_subscribe(observer: ObserverBase[str], scheduler):
        task = asyncio.run_coroutine_threadsafe(fetch_data(), loop=subscription_loop)

        def handle_result(result):
            observer.on_next(result.result())
            observer.on_completed()

        task.add_done_callback(handle_result)

        return Disposable(lambda: task.cancel())  # type: ignore

    source: Observable[int] = reactivex.interval(1)  # type: ignore

    def prefetch_data(i) -> Observable[str]:
        return create(on_subscribe)

    return source.pipe(
        ops.flat_map(prefetch_data)
    )


async def await_and_cancel():
    disposable = connect(asyncio.get_running_loop()).subscribe(on_next=print)
    await asyncio.sleep(5000)
    # print("cancelling task")

    # disposable.dispose()


if __name__ == "__main__":
    loop = asyncio.new_event_loop()

    loop.create_task(await_and_cancel())

    loop.run_forever()
