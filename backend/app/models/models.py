from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from ..database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    company_name = Column(String)
    industry = Column(String) # Manufacturing, Retail, etc.
    preferred_language = Column(String, default="en")

    reports = relationship("FinancialReport", back_populates="owner")

class FinancialReport(Base):
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Metadata about the source
    source_type = Column(String) # CSV, XLSX, API
    filename = Column(String, nullable=True)

    # Analyzed Metrics
    revenue_streams = Column(JSON) # Detailed breakdown
    cost_structure = Column(JSON) # Detailed breakdown
    key_metrics = Column(JSON) # ROI, Margins, etc.
    
    # New Dimensions
    accounts_receivable = Column(JSON)
    accounts_payable = Column(JSON)
    inventory_levels = Column(JSON)
    loan_obligations = Column(JSON)
    banking_data = Column(JSON) # Transactions/Balance from API
    tax_compliance = Column(String) # Encrypted JSON
    
    # Analysis Metadata
    industry = Column(String, default="Unknown") # E.g., Retail, Manufacturing, Services
    
    # AI Assessment
    risk_assessment = Column(String) # Low, Medium, High
    credit_score_estimate = Column(Integer)
    recommendations = Column(JSON) # List of suggestions

    owner = relationship("User", back_populates="reports")
