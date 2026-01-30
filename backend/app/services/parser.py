import pandas as pd
import io
from fastapi import HTTPException
from typing import Dict, Any

def parse_file(content: bytes, filename: str) -> pd.DataFrame:
    try:
        if filename.endswith('.csv'):
            df = pd.read_csv(io.BytesIO(content))
        elif filename.endswith('.xlsx') or filename.endswith('.xls'):
            df = pd.read_excel(io.BytesIO(content))
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format. Please upload CSV or Excel.")
        
        df = df.dropna(how='all')
        return df
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error parsing file: {str(e)}")

def extract_financial_metrics(df: pd.DataFrame) -> Dict[str, Any]:
    """
    Enhanced heuristic extraction for all data dimensions.
    """
    # Normalize column names for easier matching: lowercase, strip junk
    original_cols = df.columns
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # 3. Check for Financial Risk Assessment Dataset (Row-per-applicant)
    # Normalize column names for easier matching: lowercase, strip junk
    original_cols = df.columns
    df.columns = [str(c).lower().strip() for c in df.columns]
    
    # 3. Check for Financial Risk Assessment Dataset (Row-per-applicant)
    if "loan amount" in df.columns and "income" in df.columns and "risk rating" in df.columns:
        # This is the risk assessment dataset
        total_revenue = df["income"].sum()
        revenue_by_employment = df.groupby("employment status")["income"].sum().to_dict() if "employment status" in df.columns else {}
        
        total_loans = df["loan amount"].sum()
        loans_by_purpose = df.groupby("loan purpose")["loan amount"].sum().to_dict() if "loan purpose" in df.columns else {}
        
        avg_credit_score = df["credit score"].mean() if "credit score" in df.columns else 0
        
        # Calculate approximate yearly debt payments based on DTI * Income
        # Assuming DTI is monthly, so we infer some yearly cost
        if "debt-to-income ratio" in df.columns:
            estimated_costs = (df["debt-to-income ratio"] * df["income"]).sum()
        else:
            estimated_costs = 0
            
        risk_counts = df["risk rating"].value_counts().to_dict()
        majority_risk = df["risk rating"].mode()[0] if not df["risk rating"].empty else "Unknown"

        return {
            "revenue_streams": {
                "total": float(total_revenue),
                "categories": {k: float(v) for k, v in revenue_by_employment.items()},
                "growth": 0.0
            },
            "cost_structure": {
                "total": float(estimated_costs),
                "categories": {"Estimated Debt Service": float(estimated_costs)},
            },
            "net_profit": float(total_revenue - estimated_costs),
            "accounts_receivable": {"total": 0.0, "details": []},
            "accounts_payable": {"total": 0.0, "details": []},
            "inventory_levels": {"total": 0.0, "details": []},
            "loan_obligations": {
                "total": float(total_loans),
                "details": [{"item": k, "amount": float(v)} for k, v in loans_by_purpose.items()]
            },
            "tax_compliance": {"total": 0.0, "details": []},
            "raw_text": "Processed Financial Risk Assessment Dataset",
            # We can smuggle the risk profile into recommendations or a separate field if needed,
            # but for now let's just ensure the base keys work.
            # The AI advisor might overwrite risk_assessment, so we rely on standard metrics.
        }

    # If not a risk assessment dataset, proceed with general financial metrics extraction
    # Initialize metric containers
    metrics = {
        "revenue_streams": {"total": 0, "categories": {}},
        "cost_structure": {"total": 0, "categories": {}},
        "net_profit": 0,
        "accounts_receivable": {"total": 0, "details": []},
        "accounts_payable": {"total": 0, "details": []},
        "inventory_levels": {"total": 0, "details": []},
        "loan_obligations": {"total": 0, "details": []},
        "tax_compliance": {"total": 0, "details": []}
    }
    
    # Helper to check if row/col matches keywords
    def matches(text, keywords):
        if not isinstance(text, str): return False
        text = text.lower()
        return any(k in text for k in keywords)

    # Keywords configuration
    keywords = {
        "revenue": ["revenue", "sales", "income", "receipts"],
        "expenses": ["expense", "cost", "salary", "rent", "utilities", "marketing"],
        "receivable": ["receivable", "due from", "invoice out"],
        "payable": ["payable", "due to", "invoice in", "bill"],
        "inventory": ["inventory", "stock", "goods"],
        "loans": ["loan", "interest", "credit", "debt", "principal", "emi"],
        "tax": ["tax", "gst", "vat", "deduction", "duty"]
    }
    
    # 1. Column-based Approach (if data is pivoted, e.g. columns = [Date, Type, Amount])
    # Identify relevant columns
    cat_col = next((c for c in df.columns if matches(c, ["category", "type", "description", "item"])), None)
    amt_col = next((c for c in df.columns if matches(c, ["amount", "value", "cost", "price", "total"])), None)
    
    if cat_col and amt_col:
        # Row-wise iteration
        for _, row in df.iterrows():
            category = str(row[cat_col])
            try:
                amount = float(row[amt_col])
            except:
                continue
                
            if is_revenue := matches(category, keywords["revenue"]):
                metrics["revenue_streams"]["total"] += amount
                metrics["revenue_streams"]["categories"][category] = amount
            elif is_expense := matches(category, keywords["expenses"]):
                metrics["cost_structure"]["total"] += amount
                metrics["cost_structure"]["categories"][category] = amount
            
            # Specific dimension checks
            if matches(category, keywords["receivable"]):
                metrics["accounts_receivable"]["total"] += amount
                metrics["accounts_receivable"]["details"].append({"item": category, "amount": amount})
            if matches(category, keywords["payable"]):
                metrics["accounts_payable"]["total"] += amount
                metrics["accounts_payable"]["details"].append({"item": category, "amount": amount})
            if matches(category, keywords["inventory"]):
                metrics["inventory_levels"]["total"] += amount
                metrics["inventory_levels"]["details"].append({"item": category, "amount": amount})
            if matches(category, keywords["loans"]):
                metrics["loan_obligations"]["total"] += amount
                metrics["loan_obligations"]["details"].append({"item": category, "amount": amount})
            if matches(category, keywords["tax"]):
                metrics["tax_compliance"]["total"] += amount
                metrics["tax_compliance"]["details"].append({"item": category, "amount": amount})

    else:
        # Fallback: Column-header Approach (e.g. columns = [Sales, Rent, Taxes])
        for col in df.columns:
            try:
                col_total = df[col].sum() if pd.api.types.is_numeric_dtype(df[col]) else 0
            except:
                col_total = 0
            
            if col_total == 0: continue

            if matches(col, keywords["revenue"]):
                metrics["revenue_streams"]["total"] += col_total
                metrics["revenue_streams"]["categories"][col] = col_total
            elif matches(col, keywords["expenses"]):
                metrics["cost_structure"]["total"] += col_total
                metrics["cost_structure"]["categories"][col] = col_total
            
            if matches(col, keywords["receivable"]):
                metrics["accounts_receivable"]["total"] += col_total
            if matches(col, keywords["payable"]):
                metrics["accounts_payable"]["total"] += col_total
            if matches(col, keywords["inventory"]):
                metrics["inventory_levels"]["total"] += col_total
            if matches(col, keywords["loans"]):
                metrics["loan_obligations"]["total"] += col_total
            if matches(col, keywords["tax"]):
                metrics["tax_compliance"]["total"] += col_total

    metrics["net_profit"] = metrics["revenue_streams"]["total"] - metrics["cost_structure"]["total"]
    
    return metrics
