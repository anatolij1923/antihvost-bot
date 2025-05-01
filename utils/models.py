from datetime import datetime
from typing import Optional
from dataclasses import dataclass
from enum import Enum
import uuid

class AssignmentStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    SUBMITTED = "submitted"

@dataclass
class Assignment:
    id: str
    type: str  # 'lab' или 'homework'
    name: str
    description: str
    deadline: datetime
    created_at: datetime
    created_by: int  # ID пользователя, создавшего задание
    status: AssignmentStatus = AssignmentStatus.NOT_STARTED  # Статус выполнения задания
    subject: str = None  # Предмет (только для лабораторных работ)

class Event:
    def __init__(self, id: str, name: str, description: str, date: datetime, created_at: datetime, created_by: int):
        self.id = id
        self.name = name
        self.description = description
        self.date = date
        self.created_at = created_at
        self.created_by = created_by 