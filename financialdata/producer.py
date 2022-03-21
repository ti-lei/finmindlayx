import importlib
import sys

from loguru import logger

# import db的時候已經跟db建立了連線
from financialdata.backend import db
from financialdata.tasks.task import crawler


def Update(dataset: str, start_date: str, end_date: str):
    print(f"financialdata.crawler.{dataset}")
    # 拿取每個爬蟲任務的參數列表，
    # 包含爬蟲資料的日期 date，例如 2021-04-10 的台股股價，
    # 資料來源 data_source，例如 twse 證交所、tpex 櫃買中心
    parameter_list = getattr(
        importlib.import_module(f"financialdata.crawler.{dataset}"),
        "gen_task_paramter_list",
    )(start_date=start_date, end_date=end_date)

    # 用 for loop 發送任務
    for parameter in parameter_list:
        
        logger.info(f"{dataset}, {parameter}")
        # crawler 是從 task.py來 查詢 celery 的用法, 送出任務
        task = crawler.s(dataset, parameter)
        # queue 參數，可以指定要發送到特定 queue 列隊中
        task.apply_async(queue=parameter.get("data_source", ""))

    db.router.close_connection()


if __name__ == "__main__":
    # sys.agv 會拿到 [financialdata/producer.py, taiwan_stock_price, 2021-04-01, 2021-04-12]
    dataset, start_date, end_date = sys.argv[1:]
    Update(dataset, start_date, end_date)
