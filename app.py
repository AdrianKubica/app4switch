from fastapi import FastAPI, File, UploadFile
import pandas as pd
from starlette.staticfiles import StaticFiles

from utils.db.config import db
from utils.db.queries import create_table, delete_switch_data, insert_switch_data, calculate_data

app = FastAPI()


@app.on_event("startup")
async def connect_db():
    await db.connect()
    await create_table()


@app.on_event("shutdown")
async def disconnect_db():
    await db.disconnect()


@app.post('/api/upload')
async def upload(file: UploadFile = File(...)):
    upload_file = await file.read()
    df = pd.read_excel(upload_file, sheet_name='DATA')
    df.columns = ['host', 'name', 'key', 'itemid', 'valinmb', 'clock', 't', 'nr_week']
    await delete_switch_data()
    await insert_switch_data(df.iterrows())
    result = await calculate_data()
    return {'result': result}

app.mount('/', StaticFiles(directory="frontend/dist", html=True))
