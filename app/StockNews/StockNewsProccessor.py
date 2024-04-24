#!/usr/bin/env python
import dataclasses
from typing import Union
from reactivex import Observable, operators as ops
from app.Message.Message import Message, MessageType
from bs4 import BeautifulSoup
from app.StockNews.StockNews import StockNews

NEWS_PANEL = 'tabpanel-news'
NEWS_CLASS = 'subtle-link fin-size-small titles noUnderline svelte-wdkn18'


class StockNewsProccessor:

    @staticmethod
    def process(source: Observable[dict[str, Union[str, float]]]) -> Observable[Message[float]]:
        return source.pipe(
            ops.map(StockNewsProccessor.map_news_panel),
            ops.map(StockNewsProccessor.map_all_news),
            ops.map(StockNewsProccessor.map_to_title_and_list)
        )

    @staticmethod
    def map_to_title_and_list(event):
        """ generated source for method map_to_news """
        return StockNews.news([item['title'] for item in event[0]], [item['href'] for item in event[0]], event[1])

    @staticmethod
    def map_news_panel(event: tuple[BeautifulSoup, str]) -> tuple[BeautifulSoup, str]:
        """ generated source for method is_valid_news """
        return event[0].find(id=NEWS_PANEL), event[1]

    @staticmethod
    def map_all_news(event: tuple[BeautifulSoup, str]) -> tuple[list[BeautifulSoup], str]:
        """ generated source for method is_valid_news """
        return event[0].find_all(class_=NEWS_CLASS), event[1]
