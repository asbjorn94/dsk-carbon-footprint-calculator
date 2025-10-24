class DSKItem:
    def __init__(self, id: int = None, product: str = None, category: str = None, footprint: float = None):
        self.id = id
        self.product = product
        self.category = category
        self.footprint = footprint

    def __repr__(self):
        return f"DSKItem(id: {self.id}, product: {self.product}, category: {self.category}, footprint: {self.footprint})"

#Potentially to be used
# class DSKBaseword:
#     def __init__(self, baseword: str = None, dsk_items: list[DSKItem] = None):
#         self.baseword = baseword
#         self.dsk_items = dsk_items

#     def __repr__(self):
#         return f"DSKBaseword(baseword: {self.baseword}, dsk_items: {self.dsk_items}"