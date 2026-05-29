"""
Anomaly Watchdog – Validations
Defines the strict structure for transaction profiling and fraud detection.
"""
from datetime import datetime
from typing import List, Literal, Optional
from pydantic import BaseModel, Field

class TransactionSchema(BaseModel):
    transaction_id: str = Field(..., description="Unique identifier for the transaction")
    amount: float = Field(..., gt=0, description="Transaction amount in INR")
    category: str = Field(..., description="Category of spend (e.g., food, travel, shopping)")
    timestamp: datetime = Field(..., description="Exact date and time of the transaction")
    merchant: str = Field(..., description="Name of the merchant")

class HistoricalProfileSchema(BaseModel):
    category: str
    average_spend: float = Field(..., ge=0, description="Mean spend amount for this category")
    standard_deviation: float = Field(..., ge=0, description="Volatility/spread of spend in this category")

class AnomalyRequestPayload(BaseModel):
    current_transaction: TransactionSchema
    recent_history: List[TransactionSchema] = Field(default=[], description="Transactions in the last 24-48 hours")
    user_profiles: List[HistoricalProfileSchema] = Field(default=[], description="User's long-term baseline averages")

class AnomalyResponseSchema(BaseModel):
    is_anomaly: bool
    risk_score: float = Field(..., ge=0, le=100, description="Risk assessment score from 0 to 100")
    reasons: List[str] = Field(default=[], description="Specific triggers that marked this transaction")