from .base_exception import ApplicationException

class OrderProductNotCreatedException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Failed to create order product",
            status_code=500
        )