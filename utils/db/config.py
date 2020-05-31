from databases import Database
import os

EXCEL_TABS = ['Outgoing', 'Incoming']

DB_HOST = os.environ['POSTGRES_HOST']
DB_USER = os.environ['POSTGRES_USER']
DB_PASSWORD = os.environ['POSTGRES_PASSWORD']
DB_NAME = os.environ['POSTGRES_DB']
DB_PORT = os.environ['POSTGRES_PORT']
DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

db = Database(DB_URL)
