import csv, sys
from pathlib import Path
CODE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(CODE_DIR))
from main import Engine

engine = Engine()
with open("dataset/sample_requests.csv", encoding="utf-8") as f:
    samples = list(csv.DictReader(f))

status_match = 0
method_match = 0
plan_match = 0
earliest_match = 0
total = len(samples)

print("="*75)
print(f" BENCHMARK EVALUATION ON {total} GROUND-TRUTH SAMPLES")
print("="*75)

for s in samples:
    pred = engine.recommend(s)
    
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
    
    print(f"{s['request_id']} | Status: {status_icon} {pred['affordability_status']:20s} (Truth: {s['affordability_status']})")
    if not sm or not mm:
        print(f"   -> Method: {method_icon} Pred={pred['recommended_payment_method']} | Truth={s['recommended_payment_method']}")
        print(f"   -> Plan: Pred={pred['payment_plan']} | Truth={s['payment_plan']}")
        print(f"   -> Earliest: Pred={pred['earliest_date_for_full_payment']} | Truth={s['earliest_date_for_full_payment']}")

print("="*75)
print(f"Affordability Status Accuracy:       {status_match}/{total} ({status_match/total*100:.1f}%)")
print(f"Recommended Payment Method Accuracy: {method_match}/{total} ({method_match/total*100:.1f}%)")
print(f"Payment Plan Exact Match:            {plan_match}/{total} ({plan_match/total*100:.1f}%)")
print(f"Earliest Date Exact Match:           {earliest_match}/{total} ({earliest_match/total*100:.1f}%)")
print("="*75)
