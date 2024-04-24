import asyncio
import logging
import os.path
from typing import Any

import reactivex
import tornado.escape
import tornado.options
import tornado.web
import tornado.websocket
from reactivex import operators as ops, Subject, merge
from reactivex.abc import DisposableBase
from reactivex.subject import ReplaySubject
from tornado.options import define

from app.StockPrices.StockPriceProccessor import StockPricesProcessor
from app.StockNews.StockNewsProccessor import StockNewsProccessor
from app.Message import Message
from app.StockPrices.StockPriceTracker import connect
from app.StockNews.StockNewsTracker import connect as news_connect

define("port", default=8080, help="run on the given port", type=int)


class Application(tornado.web.Application):
    def __init__(self):
        inbound_msg = Subject()  # through this subject clients may send tick size configuration changes
        outbound_msg = ReplaySubject(20)  # cache 1 last message
        handlers = [(r"/", MainHandler),
                    (r"/stream", StreamSocketHandler, {'inbound_msg': inbound_msg, 'outbound_msg': outbound_msg})]
        settings = dict(
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            template_path=os.path.join(os.path.dirname(__file__), "ui"),
            static_path=os.path.join(os.path.dirname(__file__), "ui"),
            xsrf_cookies=True,
        )
        super().__init__(handlers, **settings)

        loop = asyncio.get_running_loop()

        def process_stock_news(source_of_prices):
            return (source_of_prices.pipe(
                ops.filter(StockPricesProcessor.trend_changed),
                ops.flat_map(lambda x: news_connect(loop).pipe(
                    lambda source: StockNewsProccessor.process(source),
                    ops.do_action(on_next=print, on_error=print)
                )
                             )
            )
            )

        (connect(loop)
        .pipe(
            ops.retry(),  # reconnect on client connection failure
            ops.share(),  # enable multiple subscriber to consume the same client connection
            lambda source: StockPricesProcessor.process(source),
            lambda source: StockPricesProcessor.remove_duplicated(source),
            ops.share(),  # enable multiple subscriber to consume the same processed prices stream
            lambda source_of_prices: reactivex.merge(source_of_prices,
                                                     process_stock_news(source_of_prices)),
            ops.do_action(on_next=print, on_error=print)
        )).subscribe(outbound_msg)


class MainHandler(tornado.web.RequestHandler):

    def check_origin(self, origin: str) -> bool:
        return False

    def get(self):
        self.render("index.html")


class StreamSocketHandler(tornado.websocket.WebSocketHandler):
    subscription: DisposableBase
    inbound_msg: Subject[int]
    outbound_msg: Subject

    def initialize(self, inbound_msg: Subject[int], outbound_msg: Subject):
        self.inbound_msg = inbound_msg
        self.outbound_msg = outbound_msg

    def check_origin(self, origin: str) -> bool:
        return True

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        self.subscription = self.outbound_msg.subscribe(on_next=lambda msg: self.send_updates(msg))

    def on_close(self):
        self.subscription.dispose()

    def send_updates(self, msg):
        try:
            self.write_message({
                'data': msg.data,
                'share': msg.share,
                'type': msg.type.name}, binary=False)
        except:
            logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        logging.info("got message %r", message)
        self.inbound_msg.on_next(int(message))


async def main():
    tornado.options.parse_command_line()
    app = Application()
    app.listen(8080)
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())


