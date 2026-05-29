"""
Anomaly Watchdog Router – DUNK.ai
Exposes transaction monitoring and real-time fraud assessment endpoints.
"""

from fastapi import APIRouter, HTTPException, status
from dunk_ai.tools.anomaly.validations import AnomalyRequestPayload, AnomalyResponseSchema
from dunk_ai.tools.anomaly.logic import evaluate_transaction_risk

router = APIRouter(
    prefix="/anomaly",
    tags=["Anomaly Watchdog Engine"]
)

@router.post("/detect", response_model=AnomalyResponseSchema, status_code=status.HTTP_200_OK)
async def detect_transaction_anomaly(payload: AnomalyRequestPayload):
    """
    Ingests a single transaction alongside contextual history, processes it through 
    the statistical risk engine, and reports immediate flags or high-velocity risk metrics.
    """
    try:
        # Run the validation payload directly into the analytical processing module
        evaluation = evaluate_transaction_risk(payload)
        return evaluation
    except ValueError as val_err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Data verification mismatch: {str(val_err)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
            detail="Error processing core anomaly detection matrices."
        )