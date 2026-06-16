from enum import Enum

class OrderStatus(Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

    @staticmethod
    def is_enable_to_change_status(current_status: "OrderStatus", new_status: "OrderStatus") -> bool:
        if current_status == OrderStatus.PENDING and new_status == OrderStatus.IN_PROGRESS:
            return True
        if current_status == OrderStatus.IN_PROGRESS and new_status == OrderStatus.COMPLETED:
            return True
        if current_status == OrderStatus.IN_PROGRESS and new_status == OrderStatus.CANCELLED:
            return True
        return False