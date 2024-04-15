from dataclasses import dataclass


@dataclass
class Product:
    id: int
    name: str
    price: float
    img: str
    link: str
    code: int
    characteristic: list

    def __init__(self, id: int, name: str, price: float, img: str,
                 link: str, code: int, characteristic: tuple):
        self.id = id
        self.name = name
        self.price = price
        self.img = img
        self.link = link
        self.code = code
        self.characteristic = characteristic

        def __str__(self):
            return f"{self.id}-{self.name}-{self.price}-{self.img}-{self.link}-{self.code}-{self.characteristic}"

    def to_dict(self) -> {}:
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "img": self.img,
            "link": self.link,
            "code": self.code,
            "characteristic": self.characteristic
        }

    @classmethod
    def from_dict(cls, attributes: dict) -> 'Product':
        return cls(**attributes)