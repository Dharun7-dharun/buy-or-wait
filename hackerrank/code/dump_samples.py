import csv
import json

with open("dataset/sample_requests.csv", encoding="utf-8") as f:
    samples = list(csv.DictReader(f))

print(f"Total samples: {len(samples)}")
for i, s in enumerate(samples[:5]):
    print(f"\nSample {i+1}: {s['request_id']} | User: {s['user_id']} | Date: {s['request_date']} | Desired: {s['desired_completion_date']}")
    print(f"  Req Amount: {s['requested_amount']} | Safe today: {s['amount_safe_to_pay']} | Status: {s['affordability_status']}")
    print(f"  Method: {s['recommended_payment_method']} | Earliest full: {s['earliest_date_for_full_payment']}")
    print(f"  Plan: {s['payment_plan']}")
    print(f"  Spending changes: {s['spending_changes_needed']}")
    print(f"  Explanation: {s['decision_explanation']}")
