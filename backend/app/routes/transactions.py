from decimal import Decimal
from fastapi import APIRouter
from pydantic import BaseModel

transactions_router: APIRouter 	= APIRouter(prefix="/transactions")

class TransactionResponse(BaseModel):
	id: int
	value: Decimal

@transactions_router.get("/")
async def index() -> TransactionResponse:
	return TransactionResponse(
		id=1,
		value=Decimal(value="100.00"),
	)
