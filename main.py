from datetime import date, datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal

class TransactionCreate(BaseModel):
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    category: str
    type: Literal["income", "expense"]
    description: str
    date: date

class Transaction(TransactionCreate):
    id: int
    created_at: datetime

app = FastAPI() # create app instance
transactions = [] #in memory list to hold transactions

@app.get("/transactions")
def get_transactions():
    return transactions

@app.post("/transactions")
def create_transactions(transaction: TransactionCreate):
    transaction_data = transaction.model_dump()
    t = Transaction(id=len(transactions) + 1, created_at=datetime.now(), **transaction_data)
    transactions.append(t)
    return t

@app.get("/transactions/{id}")
def get_transaction(id: int):
    for t in transactions:
        if t.id == id:
            return t
    raise HTTPException (
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Transaction ID '{id}' not found."
    )

@app.delete("/transactions/{id}")
def del_transaction(id: int):
    target = -1
    for i, t in enumerate(transactions):
        if t.id == id:
            target = i
            break
    if target == -1:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Transaction ID '{id}' not found."
        )
    else:
        transactions.pop(target)