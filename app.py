from fastapi import FastAPI, File, UploadFile
import pandas as pd
import asyncio
from utils.db.config import db, EXCEL_TABS
from utils.db.helpers import db_table_operation
from utils.db.queries import create_table, delete_switch_data, insert_switch_data, calculate_data

app = FastAPI()


@app.on_event("startup")
async def connect_db():
    print('start')
    await db.connect()
    tasks = db_table_operation(create_table)
    await asyncio.gather(*tasks)


@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()


@app.get('/api')
async def index():
    return {'hello': 'world'}


@app.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    upload_file = await file.read()
    xls_data = []
    for tab in EXCEL_TABS:
        df = pd.read_excel(upload_file, sheet_name=tab)
        df.columns = ['host', 'name', 'key', 'itemid', 'valinmb', 'clock', 't', 'nr_week']
        xls_data.append({'tab_name': tab, 'df': df})
    # # outgoing_xls = pd.read_excel(await file.read(), sheet_name='Outgoing')
    delete_tasks = db_table_operation(delete_switch_data)
    await asyncio.gather(*delete_tasks)
    # await delete_switch_data()
    insert_tasks = [insert_switch_data(tab_data['df'].iterrows(), tab_data['tab_name']) for tab_data in xls_data]
    await asyncio.gather(*insert_tasks)
    calculate_tasks = db_table_operation(calculate_data)
    results = await asyncio.gather(*calculate_tasks)
    print(results)
    return {'res': 10}
