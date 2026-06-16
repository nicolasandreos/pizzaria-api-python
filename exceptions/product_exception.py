from .base_exception import ApplicationException

class ProductNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Product not found",
            status_code=404
        )

class ProductAlreadyDisabledException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Product already disabled",
            status_code=400
        )

class ProductAlreadyEnabledException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Product already enabled",
            status_code=400
        )