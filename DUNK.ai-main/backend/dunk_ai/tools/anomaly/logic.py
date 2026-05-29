"""
Anomaly Watchdog Logic – DUNK.ai
Core mathematical engine for evaluating transaction risks.
"""
import math
from datetime import timedelta
from typing import Dict, Any
from .validations import AnomalyRequestPayload, AnomalyResponseSchema

def evaluate_transaction_risk(payload: AnomalyRequestPayload) -> AnomalyResponseSchema:
    tx = payload.current_transaction
    reasons = []
    risk_score = 0.0

    # 1. LAYER ONE: Statistical Category Deviation (Z-Score)
    # Formula: Z = (X - μ) / σ
    profile = next((p for p in payload.user_profiles if p.category.lower() == tx.category.lower()), None)
    if profile and profile.standard_deviation > 0:
        z_score = (tx.amount - profile.average_spend) / profile.standard_deviation
        
        if z_score > 3.0:  # Beyond 3 standard deviations is a severe outlier
            reasons.append(f"Critical spending spike in {tx.category} (Amount is {round(z_score, 1)}x volatile deviations above normal)")
            risk_score += 45.0
        elif z_score > 2.0:
            reasons.append(f"Moderate spending deviation in {tx.category}")
            risk_score += 20.0
    elif profile and tx.amount > profile.average_spend * 5:
        # Fallback if standard deviation is zero but amount is 5x the clean average
        reasons.append(f"Unusually high transaction volume vs baseline average for {tx.category}")
        risk_score += 30.0

    # 2. LAYER TWO: High-Frequency Velocity Checks
    # Look for rapid successive transactions within a tight time window
    time_window_limit = timedelta(minutes=5)
    recent_same_merchant = [
        r for r in payload.recent_history 
        if r.merchant.lower() == tx.merchant.lower() 
        and abs((tx.timestamp - r.timestamp).total_seconds()) <= time_window_limit.total_seconds()
    ]
    
    if len(recent_same_merchant) > 0:
        # Check if it's an exact duplicate amount (accidental double swipe or merchant bug)
        exact_duplicates = [r for r in recent_same_merchant if math.isclose(r.amount, tx.amount)]
        if exact_duplicates:
            reasons.append(f"Potential duplicate charge detected at {tx.merchant} within 5 minutes")
            risk_score += 40.0
        else:
            reasons.append(f"High-velocity transaction burst detected at {tx.merchant}")
            risk_score += 15.0

    # 3. LAYER THREE: Suspicious Temporal (Time) Allocation
    # Check for high-value anomalies during midnight hours (12 AM to 5 AM)
    if 0 <= tx.timestamp.hour <= 5 and tx.amount > 5000:
        reasons.append("High-value transaction executed during anomalous off-peak hours (12 AM - 5 AM)")
        risk_score += 20.0

    # Caps risk score at 100 max boundary
    final_risk = min(100.0, risk_score)
    is_anomaly = final_risk >= 40.0  # Threshold to trigger UI warnings

    return AnomalyResponseSchema(
        is_anomaly=is_anomaly,
        risk_score=round(final_risk, 2),
        reasons=reasons
    )