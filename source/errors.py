class UnitNotRecognizedError(Exception):
    pass

class IngredientNotFoundError(Exception):
    def __init__(self, error_msg : str, ingredient : str):
        self.error_msg = error_msg
        self.ingredient = ingredient

class QuantityNotStatedError(Exception):
    pass