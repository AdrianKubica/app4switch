from datetime import datetime
from pydantic import BaseModel


class SwitchData(BaseModel):
    host: str
    name: str
    key: str
    itemid: str
    valinmb: float
    clock: datetime
    t: datetime
    nr_week: int
