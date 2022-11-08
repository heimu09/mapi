from fastapi import FastAPI, Depends

from sqlalchemy import select
from sqlmodel import Session

from app.db import init_db, get_session
from app.models import *

app = FastAPI()


@app.on_event('startup')
def on_startup():
    init_db()


@app.get('/ping')
def pong():
    return {'ping': 'pong'}

@app.get('/workers', response_model=list[Worker])
def get_workers(session: Session = Depends(get_session)):
    result = session.execute(select(Worker))
    workers = result.scalars().all()
    return [Worker(name=worker.name, phone_number=worker.phone_number, id=worker.id, trade_point=worker.trade_point) for worker in workers]


@app.post('/workers')
def add_worker(worker: WorkerCreate, session: Session = Depends(get_session)):
    worker = Worker(name=worker.name, phone_number=worker.phone_number, trade_point=worker.trade_point)
    session.add(worker)
    session.commit()
    session.refresh(worker)
    return worker


@app.post('/trade_points', response_model=list[TradePoint])
def get_trade_points(trade_point: TradePointGet, session: Session = Depends(get_session)):
    workers = session.execute(select(Worker).where(Worker.phone_number == trade_point.phone_number))
    workers_id = [worker[0].id for worker in workers]
    worker_trade_points = session.execute(select(WorkerTradePoint).where(WorkerTradePoint.worker_id in workers_id))
    worker_trade_point_ids = [worker_trade_point[0].id for worker_trade_point in worker_trade_points]
    trade_points = session.execute(select(TradePoint).where(TradePoint.id in worker_trade_point_ids))
    
    return [Worker(trade_point) for trade_point in trade_points]
