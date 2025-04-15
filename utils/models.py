from datetime import datetime
from typing import Optional
from dataclasses import dataclass

@dataclass
class Assignment:
    id: str
    type: str  # 'lab' или 'homework'
    name: str
    description: str
    deadline: datetime
    created_at: datetime
    created_by: int  # ID пользователя, создавшего задание 