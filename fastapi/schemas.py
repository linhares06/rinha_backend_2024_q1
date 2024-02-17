from pydantic import BaseModel


class Client(BaseModel):
    id: int
    limit: int
    opening_balance: int