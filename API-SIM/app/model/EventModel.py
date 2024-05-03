from pydantic import BaseModel


class EventModel(BaseModel):
    id_event: int
    event_name: str
    event_pound: float