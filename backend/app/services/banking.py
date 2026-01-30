from typing import Dict, Any, List
import random
from datetime import datetime, timedelta

class BankingProvider:
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        raise NotImplementedError

class MockPlaid(BankingProvider):
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        # Simulate last 30 days transactions
        txs = []
        categories = ["Rent", "Utilities", "Salary", "Vendor Payment", "Subscription"]
        for i in range(10):
            txs.append({
                "date": (datetime.now() - timedelta(days=i*3)).strftime("%Y-%m-%d"),
                "amount": round(random.uniform(-5000, 10000), 2),
                "description": f"Txn Ref: {random.randint(1000,9999)} - {random.choice(categories)}",
                "category": random.choice(categories)
            })
        return txs

class MockStripe(BankingProvider):
    def get_transactions(self, account_id: str) -> List[Dict[str, Any]]:
        # Simulate stripe payouts
        txs = []
        for i in range(5):
            txs.append({
                "date": (datetime.now() - timedelta(days=i*7)).strftime("%Y-%m-%d"),
                "amount": round(random.uniform(1000, 5000), 2),
                "description": f"Payout #{random.randint(10000,99999)}",
                "type": "payout"
            })
        return txs

def fetch_banking_data(provider_name: str, account_id: str) -> Dict[str, Any]:
    if provider_name.lower() == "plaid":
        provider = MockPlaid()
    elif provider_name.lower() == "stripe":
        provider = MockStripe()
    else:
        return {"error": "Unknown provider"}
    
    return {
        "provider": provider_name,
        "account_id": account_id,
        "balance": round(random.uniform(10000, 500000), 2),
        "transactions": provider.get_transactions(account_id),
        "last_sync": datetime.now().isoformat()
    }
