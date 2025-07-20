from pydantic import BaseModel, validator
from datetime import datetime

class Receipt(BaseModel):
    vendor: str
    date: str
    amount: float
    currency: str = "INR"

    @validator("date")
    def check_date(cls, v):
        try:
            datetime.strptime(v, "%d/%m/%Y")
            return v
        except Exception:
            raise ValueError("Date must be in DD/MM/YYYY format")

    @validator("amount")
    def check_amount(cls, v):
        if v < 0:
            raise ValueError("Amount must be non-negative")
        return v
