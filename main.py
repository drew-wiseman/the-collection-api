from datetime import date, datetime
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal, Optional

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
def get_transactions(
    category: Optional[str] = None, 
    type:Optional[str] = None,
    min_amount: Optional[float] = None,
    max_amount: Optional[float] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None
):
    result = transactions
    if category is not None:
        result = [t for t in result if t.category == category]
    if type is not None:
        result = [t for t in result if t.type == type]
    if min_amount is not None:
        result = [t for t in result if t.amount >= min_amount]
    if max_amount is not None:
        result = [t for t in result if t.amount <= max_amount]
    if start_date is not None:
        result = [t for t in result if t.date >= start_date]
    if end_date is not None:
        result = [t for t in result if t.date <= end_date]
    return result

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