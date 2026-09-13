import csv
from datetime import date, timedelta
from collections import defaultdict, Counter
import sys
from pathlib import Path
CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
from main import Engine

class ImprovedEngine(Engine):
    def stream_specs(self, uid, req_date):
        """Infer stable recurring streams from settled history, filtering one-offs."""
        groups = defaultdict(list)
        for e in self.by_user[uid]:
            if e.amount is None or e.status != "settled" or e.cash_date > req_date:
                continue
            # Ignore explicit one-offs: bonus, arrears, refund
            if any(w in (e.description or "").lower() for w in ["bonus", "arrears", "refund"]):
                continue
            groups[(e.event_type, e.category, e.direction, e.flexibility)].append(e)
            
        specs = []
        for key, arr in groups.items():
            arr.sort(key=lambda e: e.cash_date)
            # If monthly (intervals ~28-31 days) or regular, allow len >= 2
            if len(arr) < 2:
                continue
            dates = [e.cash_date for e in arr]
            intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            
            # Check cadence
            c = Counter(intervals)
            cadence = int(round(c.most_common(1)[0][0]))
            
            # Allow monthly cadence if intervals are in 28-31
            is_monthly = all(27 <= inv <= 32 for inv in intervals)
            if is_monthly:
                cadence = 30
            elif cadence not in {5, 7, 10, 14, 21, 28, 29, 30, 31}:
                continue
            elif len(arr) >= 5 and sum(abs(x - cadence) <= 1 for x in intervals[-5:]) < max(3, len(intervals[-5:]) - 1):
                continue
                
            avg_amt = sum(e.amount for e in arr[-5:]) / min(5, len(arr[-5:]))
            specs.append({
                "key": key,
                "history": arr,
                "cadence": cadence,
                "amount": avg_amt
            })
            
        # Also, check if next confirmed salary exists and user only has 1 settled salary
        # (like user_01 where event_25 is settled and event_103 is scheduled)
        sal_events = [e for e in self.by_user[uid] if e.category == "salary" and e.amount is not None and not any(w in (e.description or "").lower() for w in ["bonus", "arrears", "refund"])]
        if not any(s["key"][1] == "salary" for s in specs) and sal_events:
            sal_events.sort(key=lambda e: e.cash_date)
            last_sal = sal_events[-1]
            specs.append({
                "key": (last_sal.event_type, "salary", "credit", "fixed"),
                "history": sal_events,
                "cadence": 30,
                "amount": last_sal.amount
            })
            
        return specs

e = ImprovedEngine()
with open("dataset/sample_requests.csv", encoding="utf-8") as f:
    samples = list(csv.DictReader(f))

status_match = 0
method_match = 0
plan_match = 0
earliest_match = 0
total = len(samples)

print("="*75)
print(f" TESTING IMPROVED ENGINE ON {total} GROUND-TRUTH SAMPLES")
print("="*75)

for s in samples:
    pred = e.recommend(s)
    
    sm = pred['affordability_status'] == s['affordability_status']
    mm = pred['recommended_payment_method'] == s['recommended_payment_method']
    pm = pred['payment_plan'] == s['payment_plan']
    em = (pred['earliest_date_for_full_payment'] or '') == (s['earliest_date_for_full_payment'] or '')
    
    if sm: status_match += 1
    if mm: method_match += 1
    if pm: plan_match += 1
    if em: earliest_match += 1
    
    status_icon = "[PASS]" if sm else "[FAIL]"
    method_icon = "[PASS]" if mm else "[FAIL]"
    
    print(f"{s['request_id']} | Status: {status_icon} {pred['affordability_status']:20s} (Truth: {s['affordability_status']}) | Method: {method_icon} {pred['recommended_payment_method']}")

print("="*75)
print(f"Affordability Status Accuracy:       {status_match}/{total} ({status_match/total*100:.1f}%)")
print(f"Recommended Payment Method Accuracy: {method_match}/{total} ({method_match/total*100:.1f}%)")
print(f"Payment Plan Exact Match:            {plan_match}/{total} ({plan_match/total*100:.1f}%)")
print(f"Earliest Date Exact Match:           {earliest_match}/{total} ({earliest_match/total*100:.1f}%)")
print("="*75)
