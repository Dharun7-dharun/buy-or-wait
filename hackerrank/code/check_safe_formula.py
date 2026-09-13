import csv

with open('dataset/sample_requests.csv', encoding='utf-8') as f:
    samples = list(csv.DictReader(f))

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r for r in csv.DictReader(f)}

print("Comparing current_balance - min_balance with amount_safe_to_pay:")
for s in samples:
    p = profiles[s['user_id']]
    curr_bal = float(p['current_available_balance'])
    min_bal = float(p['minimum_balance_to_keep'])
    req_amt = float(s['requested_amount'])
    safe_today = float(s['amount_safe_to_pay'])
    diff = curr_bal - min_bal
    capped_diff = min(req_amt, max(0.0, diff))
    match = abs(capped_diff - safe_today) < 1e-4
    print(f"{s['request_id']} ({s['user_id']}): diff={diff:.2f}, capped={capped_diff:.2f}, safe_today={safe_today:.2f}, match={match}")
