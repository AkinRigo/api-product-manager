class NotFoundError(Exception):
    """Recurso não encontrado."""


class ConflictError(Exception):
    """Conflito com uma regra de negócio ou dado existente."""


class StockProductNotFoundError(NotFoundError):
    pass


class StockMovementNotFoundError(NotFoundError):
    pass


class InactiveProductError(ConflictError):
    pass


class InsufficientStockError(ConflictError):
    pass


class CategoryNotFoundError(NotFoundError):
    pass


class CategoryNameAlreadyExistsError(ConflictError):
    pass


class CategoryInUseError(ConflictError):
    pass


class ProductNotFoundError(NotFoundError):
    pass


class ProductSkuAlreadyExistsError(ConflictError):
    pass


class ProductCategoryNotFoundError(NotFoundError):
    pass