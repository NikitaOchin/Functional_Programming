#!/usr/bin/env python
import dataclasses
import time
from enum import Enum
from typing import TypeVar, Generic, Union
from reactivex import Observable, operators as ops


_T = TypeVar("_T")


class MessageType(Enum):
    STOCK = 0
    NEWS = 1


@dataclasses.dataclass
class Message(Generic[_T]):
    share: str
    data: _T
    type: 'MessageType'
