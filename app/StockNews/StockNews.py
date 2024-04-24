#!/usr/bin/env python
import dataclasses
from typing import Union
from reactivex import Observable, operators as ops
from app.Message.Message import Message, MessageType


@dataclasses.dataclass
class StockNews(Message):
    @staticmethod
    def news(news_title: list[str], link: list[str], share: str):
        return StockNews(data=[{'title': news_title,
                                'link': link,
                                } for news_title, link
                               in zip(news_title, link)],
                         type=MessageType.NEWS,
                         share=share)
