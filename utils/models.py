from datetime import datetime
from typing import Optional
from dataclasses import dataclass
import uuid

@dataclass
class Assignment:
    id: str
    type: str  # 'lab' или 'homework'
    name: str
    description: str
    deadline: datetime
    created_at: datetime
    created_by: int  # ID пользователя, создавшего задание 

class Event:
    def __init__(self, id: str, name: str, description: str, date: datetime, created_at: datetime, created_by: int):
        self.id = id
        self.name = name
        self.description = description
        self.date = date
        self.created_at = created_at
        self.created_by = created_by 