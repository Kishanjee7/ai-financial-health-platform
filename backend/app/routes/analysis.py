from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import FinancialReport
from ..schemas import schemas
from ..services import parser, ai_advisor
from ..core import security

router = APIRouter()

@router.post("/upload", response_model=schemas.ReportResponse)
async def upload_financial_data(
    file: UploadFile = File(...), 
    language: str = "en",
    db: Session = Depends(get_db)
):
    contents = await file.read()
    
    # Parse file
    try:
        df = parser.parse_file(contents, file.filename)
        metrics = parser.extract_financial_metrics(df)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # AI Analysis
    analysis_result = ai_advisor.analyze_financial_health(metrics, language)
    
    # Create Report with Encrypted Data
    # We serialize and encrypt the JSON buckets to protect sensitive info at rest
    new_report = FinancialReport(
        user_id=1, # Hardcoded for prototyping
        source_type="file",
        filename=file.filename,
        
        # Encrypt sensitive JSON data
        revenue_streams=security.encrypt_data(metrics["revenue_streams"]),
        cost_structure=security.encrypt_data(metrics["cost_structure"]),
        key_metrics=metrics["net_profit"], # This one is just a float/simple dict, keeping it open for quick querying or encrypt if needed
        
        accounts_receivable=security.encrypt_data(metrics["accounts_receivable"]),
        accounts_payable=security.encrypt_data(metrics["accounts_payable"]),
        inventory_levels=security.encrypt_data(metrics["inventory_levels"]),
        loan_obligations=security.encrypt_data(metrics["loan_obligations"]),
        tax_compliance=security.encrypt_data(metrics["tax_compliance"]),
        
        risk_assessment=analysis_result["risk_assessment"], # Open for querying
        credit_score_estimate=analysis_result["credit_score_estimate"],
        recommendations=security.encrypt_data(analysis_result["recommendations"])
    )
    
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    
    return new_report

@router.get("/{report_id}", response_model=schemas.ReportResponse)
async def get_report(report_id: int, db: Session = Depends(get_db)):
    report = db.query(FinancialReport).filter(FinancialReport.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # Decrypt fields for the response
    # We create a new dict or copy to avoid modifying the DB object in session
    response_data = {
        "id": report.id,
        "filename": report.filename,
        "created_at": report.created_at,
        "risk_assessment": report.risk_assessment,
        "credit_score_estimate": report.credit_score_estimate,
        # Decrypt sensitive fields
        "revenue_streams": security.decrypt_data(report.revenue_streams),
        "cost_structure": security.decrypt_data(report.cost_structure),
        "key_metrics": report.key_metrics if isinstance(report.key_metrics, dict) else {"net_profit": report.key_metrics}, # Handle legacy/types
        "accounts_receivable": security.decrypt_data(report.accounts_receivable),
        "accounts_payable": security.decrypt_data(report.accounts_payable),
        "inventory_levels": security.decrypt_data(report.inventory_levels),
        "loan_obligations": security.decrypt_data(report.loan_obligations),
        "tax_compliance": security.decrypt_data(report.tax_compliance),
        "recommendations": security.decrypt_data(report.recommendations)
    }
    
    return response_data
