from typing import Optional
from sqlmodel import SQLModel, Field

import datetime

class TradePointBase(SQLModel):
    name: str


class TradePoint(TradePointBase, table=True):
    id: int = Field(default=None, primary_key=True)


class TradePointCreate(TradePointBase):
    pass


class WorkerBase(SQLModel):
    name: str
    phone_number: str


class Worker(WorkerBase, table=True):
    id: int = Field(default=None, primary_key=True)


class WorkerCreate(WorkerBase):
    pass


class WorkerTradePointBase(SQLModel):
    trade_point_id: Optional[int] = Field(default=None, foreign_key="tradepoint.id")
    worker_id: Optional[int] = Field(default=None, foreign_key='worker.id')


class WorkerTradePoint(WorkerTradePointBase, table=True):
    id: int = Field(default=None, primary_key=True)


class WorkerTradePointCreate(WorkerTradePointBase):
    pass


class TradePointGet(SQLModel):
    phone_number: str


class CustomerBase(SQLModel):
    name: str
    phone_number: str
    trade_point_id: Optional[int] = Field(default=None, foreign_key="tradepoint.id")


class Customer(CustomerBase, table=True):
    id: int = Field(default=None, primary_key=True)


class CustomerCreate(CustomerBase):
    pass


class OrderBase(SQLModel):
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    ended: datetime.datetime = Field(default_factory=datetime.datetime.today() + datetime.timedelta(1), nullable=False)
    where: Optional[int] = Field(default=None, foreign_key="tradepoint.id")
    author: Optional[int] = Field(default=None, foreign_key="customer.id")
    status: str
    executor: Optional[int] = Field(default=None, foreign_key="worker.id")


class Order(OrderBase, table=True):
    id: int = Field(default=None, primary_key=True)


class OrderCreate(OrderBase):
    pass


class VisitedBase(SQLModel):
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow, nullable=False)
    order: Optional[int] = Field(default=None, foreign_key="order.id")
    where: Optional[int] = Field(default=None, foreign_key="tradepoint.id")
    author: Optional[int] = Field(default=None, foreign_key="customer.id")
    executor: Optional[int] = Field(default=None, foreign_key="worker.id")


class Visited(VisitedBase, table=True):
    id: int = Field(default=None, primary_key=True)


class VisitedCreate(VisitedBase):
    pass
