import asyncio

from utils.db.config import EXCEL_TABS


def db_table_operation(async_func):
    return [asyncio.create_task(async_func(table_name)) for table_name in list(map(lambda x: x.lower(), EXCEL_TABS))]
