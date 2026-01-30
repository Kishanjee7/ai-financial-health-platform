import os
from typing import Dict, Any

import json
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_financial_health(metrics: Dict[str, Any], language: str = "en") -> Dict[str, Any]:
    """
    Analyzes financial health using OpenAI if API key is present, otherwise uses fallback logic.
    """
    if os.getenv("OPENAI_API_KEY"):
        try:
            return _analyze_with_llm(metrics, language)
        except Exception as e:
            print(f"LLM Error: {e}. Falling back to rule-based logic.")
            return _analyze_rule_based(metrics, language)
    else:
        return _analyze_rule_based(metrics, language)

def _analyze_with_llm(metrics: Dict[str, Any], language: str) -> Dict[str, Any]:
    # Prune heavy data for the prompt
    summary_metrics = {k: v for k, v in metrics.items() if k not in ['raw_text']}
    
    prompt = f"""
    You are a financial advisor AI for SMEs. Analyze the following financial data for a {metrics.get('industry', 'General')} business.
    Output Language: {language} (Ensure all output text is in this language).
    
    Data:
    {json.dumps(summary_metrics, indent=2)}
    
    Return a JSON object with this exact structure:
    {{
        "risk_assessment": "Low" | "Medium" | "High" (or localized equivalent),
        "credit_score_estimate": integer (300-900),
        "recommendations": ["string", "string", "string"],
        "analysis_summary": "One sentence summary"
    }}
    """
    
    response = client.chat.completions.create(
        model="gpt-4o", # or gpt-3.5-turbo if cost is concern
        messages=[{"role": "system", "content": "You are a helpful financial expert."}, {"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    
    content = response.choices[0].message.content
    return json.loads(content)

def _analyze_rule_based(metrics: Dict[str, Any], language: str) -> Dict[str, Any]:
    revenue = metrics.get('revenue_streams', {}).get('total', 0)
    profit = metrics.get('net_profit', 0)
    inventory = metrics.get('inventory_levels', {}).get('total', 0)
    debt = metrics.get('loan_obligations', {}).get('total', 0)
    industry = metrics.get('industry', 'General')
    
    # 1. Risk Assessment
    if profit < 0 or debt > (revenue * 0.6):
        risk = "High" if language == "en" else "उच्च (High)"
        score = 550
    elif profit < (revenue * 0.1):
        # Stricter margin requirements for Services vs Retail
        threshold = 0.15 if industry == "Services" else 0.05
        if profit < (revenue * threshold):
             risk = "Medium" if language == "en" else "मध्य (Medium)"
             score = 650
        else:
             risk = "Low" if language == "en" else "कम (Low)"
             score = 750
    else:
        risk = "Low" if language == "en" else "कम (Low)"
        score = 750

    # 3. Recommendations
    recs = []
    
    # Industry Specific Advice
    if language == "en":
        if industry == "Retail" or industry == "Manufacturing":
            if inventory > (revenue * 0.4):
                 recs.append("Inventory levels are high relative to revenue. Optimize stock turnover.")
        if industry == "Services":
             recs.append("Focus on client retention and recurring revenue models.")
        if industry == "Agriculture":
             recs.append("Review crop insurance and government subsidy options.")
             
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
