import datetime
from utils.db.config import db


async def create_table():
    query = """
    CREATE TABLE IF NOT EXISTS data(
        id SERIAL,
        host TEXT,
        name TEXT,
        key TEXT,
        itemid INT,
        valinmb FLOAT(4),
        clock TIMESTAMP,
        t TEXT,
        nr_week INT
    )
    """
    await db.execute(query=query, values=None)


def transform_switch_data_record(switch_data_record):
    (_, switch_data_record) = switch_data_record
    switch_data_record = switch_data_record.to_dict()
    switch_data_record['clock'] = datetime.datetime.fromtimestamp(switch_data_record['clock'])
    return switch_data_record


async def insert_switch_data(switch_data):
    query = """
        INSERT INTO data(host, name, key, itemid, valinmb, clock, t, nr_week)
        values(:host, :name, :key, :itemid, :valinmb, :clock, :t, :nr_week)
    """
    switch_data_transformed = list(map(transform_switch_data_record, switch_data))
    await db.execute_many(query=query, values=switch_data_transformed)


async def delete_switch_data():
    query = """
    DELETE FROM data
    """
    await db.execute(query=query, values=None)


async def calculate_data():
    query = """
    SELECT data1.*, data2.avg_day, data3.avg_week
    FROM
        (SELECT key, nr_week, left(t, 10) as day, COUNT(*) as observation_counter
        FROM data
        GROUP BY key, nr_week, left(t, 10)
        ORDER BY key, nr_week, day) as data1
        LEFT JOIN

        (SELECT key, nr_week, left(t, 10) as day, AVG(valinmb) as avg_day
        FROM (SELECT *
        FROM
           (SELECT *, row_number() over (PARTITION BY key, nr_week, left(t, 10) ORDER BY valinmb DESC) as rank
            FROM data) as data_ranked
        WHERE rank BETWEEN 15 AND 26) as data_stats
        GROUP BY key, nr_week, left(t, 10)
        ORDER BY key, nr_week, day) as data2

        ON data1.key = data2.key AND data1.nr_week = data2.nr_week AND data1.day = data2.day

        LEFT JOIN

        (SELECT key, nr_week, AVG(valinmb) as avg_week
        FROM (SELECT *
        FROM
           (SELECT *, row_number() over (PARTITION BY key, nr_week, left(t, 10) ORDER BY valinmb DESC) as rank
            FROM data) as data_ranked
        WHERE rank BETWEEN 15 AND 26) as data_stats
        GROUP BY key, nr_week
        ORDER BY key, nr_week) as data3

        ON data1.key = data3.key AND data1.nr_week = data3.nr_week;
    """
    result = await db.fetch_all(query=query, values=None)
    return [dict(row) for row in result]

