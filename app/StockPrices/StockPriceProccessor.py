#!/usr/bin/env python
import dataclasses
from typing import Union
from reactivex import Observable, operators as ops
from app.Message.Message import Message, MessageType
from app.StockPrices.StockPrice import StockPrice

""" generated source for class MessageMapper """
CHART_KEY: str = "chart"
RESULT_KEY: str = "result"
META_KEY: str = 'meta'
SYMBOL_KEY: str = "symbol"
TIMESTAMP_KEY: str = "timestamp"
INDICATORS_KEY: str = "indicators"
QUOTE_KEY: str = "quote"
HIGH_KEY: str = "high"
LOW_KEY: str = "low"
OPEN_KEY: str = "open"
CLOSE_KEY: str = "close"
VOLUME_KEY: str = "volume"


class StockPricesProcessor:
    @staticmethod
    def trend_changed(source):
        try:
            result = abs(source.data[-1]['close'] / source.data[-2]['close'] - 1)
            return result > 0.0003
            # return True
        except Exception:
            return False

    @staticmethod
    def remove_duplicated(source):
        return source.pipe(
            ops.scan(lambda acc, current: (current, current == acc[0]), (None, False)),
            ops.filter(lambda x: not x[1]),
            ops.map(lambda x: x[0]),
        )

    @staticmethod
    def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
        return source.pipe(
            ops.filter(StockPricesProcessor.is_valid_price_message),
            ops.map(StockPricesProcessor.map_to_price_message)
        )

    @staticmethod
    def map_to_price_message(event) -> StockPrice[float]:
        """ generated source for method mapToPriceMessage """
        chart_result = event[CHART_KEY][RESULT_KEY][0]
        indicators = chart_result[INDICATORS_KEY][QUOTE_KEY][0]
        return StockPrice.create(
            share=chart_result[META_KEY][SYMBOL_KEY],
            timestamp=chart_result[TIMESTAMP_KEY],
            high=indicators[HIGH_KEY],
            low=indicators[LOW_KEY],
            open=indicators[OPEN_KEY],
            close=indicators[CLOSE_KEY]
        )

    @staticmethod
    def is_valid_price_message(event: dict[str, Union[str, float]]):
        """ generated source for method isValidPriceMessage """
        return (CHART_KEY in event and
                RESULT_KEY in event[CHART_KEY] and
                META_KEY in event[CHART_KEY][RESULT_KEY][0] and
                SYMBOL_KEY in event[CHART_KEY][RESULT_KEY][0][META_KEY] and
                TIMESTAMP_KEY in event[CHART_KEY][RESULT_KEY][0] and
                INDICATORS_KEY in event[CHART_KEY][RESULT_KEY][0] and
                QUOTE_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY] and
                HIGH_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY][QUOTE_KEY][0] and
                LOW_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY][QUOTE_KEY][0] and
                OPEN_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY][QUOTE_KEY][0] and
                CLOSE_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY][QUOTE_KEY][0] and
                VOLUME_KEY in event[CHART_KEY][RESULT_KEY][0][INDICATORS_KEY][QUOTE_KEY][0])
