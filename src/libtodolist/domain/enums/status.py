from enum import Enum


class StatusLabel(Enum):
    IN_PROGRESS = 'In Progress'
    COMPLETED = 'Completed'
    NEW = 'New'
    CANCELLED = 'Canceled'
