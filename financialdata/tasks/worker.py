from celery import Celery
from financialdata.config import (
    WORKER_ACCOUNT,
    WORKER_PASSWORD,
    MESSAGE_QUEUE_HOST,
    MESSAGE_QUEUE_PORT,
)

broker = (
    f"pyamqp://{WORKER_ACCOUNT}:{WORKER_PASSWORD}@"
    f"{MESSAGE_QUEUE_HOST}:{MESSAGE_QUEUE_PORT}/"
)

# app class 裡面應該含有這個建構子
# class app:
#     def __init__(self, func):
#         self.task = func

app = Celery(
    "task",
    include=["financialdata.tasks.task"],
    broker=broker,
)
