from pydantic import BaseModel, EmailStr


class CustomerCreate(BaseModel):
    customer_id: str
    name: str
    phone: str
    email: EmailStr


class CustomerResponse(CustomerCreate):
    id: int

    class Config:
        from_attributes = True