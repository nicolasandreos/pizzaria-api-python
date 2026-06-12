from .base_exception import BaseException

class ProductNotFoundException(BaseException):
    def __init__(self):
        super().__init__(
            message="Product not found",
            status_code=404
        )