from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class UserBase(BaseModel):
    email: str
    company_name: Optional[str] = None
    industry: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    
    class Config:
        orm_mode = True

class ReportBase(BaseModel):
    source_type: str
    filename: Optional[str] = None

class ReportResponse(ReportBase):
    id: int
    created_at: datetime
    revenue_streams: Optional[Dict[str, Any]]
    cost_structure: Optional[Dict[str, Any]]
    key_metrics: Optional[Dict[str, Any]]
    
    accounts_receivable: Optional[Dict[str, Any]]
    accounts_payable: Optional[Dict[str, Any]]
    inventory_levels: Optional[Dict[str, Any]]
    loan_obligations: Dict[str, Any]
    banking_data: Optional[Dict[str, Any]]
    tax_compliance: Dict[str, Any]
    
    industry: str
    risk_assessment: str
    credit_score_estimate: int
    recommendations: Optional[List[str]]

    class Config:
        orm_mode = True
