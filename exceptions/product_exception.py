from .base_exception import ApplicationException

class ProductNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Product not found",
            status_code=404
        )