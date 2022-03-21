import time
# typing?
import typing

from loguru import logger
from sqlalchemy import engine
from financialdata.backend.db import clients

# 利用簡易的sql指令確定跟sql引擎是通的
def check_alive(connect: engine.base.Connection):
    connect.execute("SELECT 1 + 1")


#函數使用返回原函數的意思? 再一次確定這個 connection work 成功
def check_connect_alive(
    connect: engine.base.Connection,
    connect_func: typing.Callable,
):
    if connect:
        try:
            check_alive(connect)
            return connect
        except Exception as e:
            logger.info(
                f"""
                {connect_func.__name__} reconnect, error: {e}
                """
            )
            time.sleep(1)
            try:
                connect = connect_func()
            except Exception as e:
                logger.info(
                    f"""
                    {connect_func.__name__} connect error, error: {e}
                    """
                )
            # 再一次確定這個 connection work 成功
            return check_connect_alive(connect, connect_func)


class Router:
    # Router 在初始化的時候就跟 clients 的 db 建立連線
    def __init__(self):
        self._mysql_financialdata_conn = clients.get_mysql_financialdata_conn()

    def check_mysql_financialdata_conn_alive(self):
        self._mysql_financialdata_conn = check_connect_alive(
            self._mysql_financialdata_conn,
            clients.get_mysql_financialdata_conn,
        )
        return self._mysql_financialdata_conn

    # 這裡property 的作用是 讓函數可以讀取但不能修改物件裡面的屬性
    # https://www.programiz.com/python-programming/property
    @property
    def mysql_financialdata_conn(self):
        return self.check_mysql_financialdata_conn_alive()

    def close_connection(self):
        self._mysql_financialdata_conn.close()
