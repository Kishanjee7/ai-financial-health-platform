import os
from typing import Dict, Any

def analyze_financial_health(metrics: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
    """
    Simulates AI analysis of financial health.
    In a real app, this would call OpenAI/Claude API with the language parameter.
    """
    revenue = metrics.get('revenue_streams', {}).get('total', 0)
    profit = metrics.get('net_profit', 0)
    inventory = metrics.get('inventory_levels', {}).get('total', 0)
    debt = metrics.get('loan_obligations', {}).get('total', 0)
    
    # 1. Risk Assessment
    if profit < 0 or debt > (revenue * 0.6):
        risk = "High" if language == "en" else "उच्च (High)"
        score = 550
    elif profit < (revenue * 0.1):
        risk = "Medium" if language == "en" else "मध्य (Medium)"
        score = 650
    else:
        risk = "Low" if language == "en" else "कम (Low)"
        score = 750

    # 3. Recommendations
    recs = []
    
    # English Logic
    if language == "en":
        if inventory > (revenue * 0.3) and revenue > 0:
            recs.append("High inventory levels detected (Over 30% of revenue). Consider JIT strategies.")
        
        if debt > 0:
            recs.append(f"Debt obligation found: ${debt}. Ensure adequate cash flow service coverage.")
            
        if metrics.get('tax_compliance', {}).get('total', 0) == 0:
            recs.append("No tax records found. Ensure GST/Tax compliance is up to date.")

        if profit < 0:
            recs.append("Immediate cost-cutting required. Review operational expenses.")
        else:
            recs.append("Consider reinvesting profits into marketing to scale revenue.")
            
    # Hindi Logic (Mock)
    else:
        if inventory > (revenue * 0.3) and revenue > 0:
            recs.append("उच्च इन्वेंट्री स्तर पाया गया। (High inventory detected)")
        
        if debt > 0:
            recs.append(f"ऋण दायित्व पाया गया: ${debt}। कृपया नकदी प्रवाह सुनिश्चित करें।")
            
        if metrics.get('tax_compliance', {}).get('total', 0) == 0:
            recs.append("कोई कर रिकॉर्ड नहीं मिला। सुनिश्चित करें कि GST/Tax अनुपालन अद्यतित है।")

        if profit < 0:
            recs.append("तत्काल लागत में कटौती आवश्यक है। परिचालन व्यय की समीक्षा करें।")
        else:
            recs.append("राजस्व बढ़ाने के लिए मुनाफे को मार्केटिंग में निवेश करने पर विचार करें।")

    return {
        "risk_assessment": risk,
        "credit_score_estimate": score,
        "recommendations": recs,
         "analysis_summary": f"Based on revenue of {revenue} and profit of {profit}, the business is in {risk} risk category."
    }
