from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: str
    description: str
    price: int


class ProductCreate(ProductBase):
    ...


class ProductUpdate(ProductBase):
    ...


class ProductUpdatePartial(ProductBase):
    name: str | None  = None
    description: str | None = None
    price: int | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
