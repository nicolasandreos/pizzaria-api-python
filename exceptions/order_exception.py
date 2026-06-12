from .base_exception import BaseException

class OrderNotCreatedException(BaseException):
    def __init__(self):
        super().__init__(
            message="Failed to create order",
            status_code=500
        )