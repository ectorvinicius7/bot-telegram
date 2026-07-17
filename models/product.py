class Product:

    def __init__(
        self,
        name,
        price_current,
        price_old,
        discount,
        url,
        store
    ):
        self.name = name
        self.price_current = price_current
        self.price_old = price_old
        self.discount = discount
        self.url = url
        self.store = store