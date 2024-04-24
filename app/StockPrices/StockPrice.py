#!/usr/bin/env python
import dataclasses
from typing import Union
from reactivex import Observable, operators as ops
from app.Message.Message import Message, MessageType
from typing import TypeVar, Generic, Union

_T = TypeVar("_T")


@dataclasses.dataclass
class StockPrice(Message[_T]):

    @staticmethod
    def create(share: str,
               timestamp: int,
               high: float,
               low: float,
               open: float,
               close: float):
        return StockPrice(share=share,
                          data=[{'dateTime': ts,
                                 'open': open,
                                 'high': high,
                                 'low': low,
                                 'close': close
                                 } for ts, high, low, open, close
                                in zip(timestamp, high, low, open, close)],
                          type=MessageType.STOCK)
