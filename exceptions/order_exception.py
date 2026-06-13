from .base_exception import ApplicationException

class OrderNotCreatedException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Failed to create order",
            status_code=500
        )

class OrderNotFoundException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Order not found",
            status_code=404
        )

class OrderNotAuthorizedToCancelException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="You are not authorized to cancel this order",
            status_code=403
        )

class OrderNotValidToCancelException(ApplicationException):
    def __init__(self):
        super().__init__(
            message="Order is not valid to cancel",
            status_code=400
        )