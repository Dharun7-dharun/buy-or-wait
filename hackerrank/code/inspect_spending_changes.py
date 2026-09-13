import csv

def inspect_user(uid, req_id):
    with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
        profiles = {r['user_id']: r for r in csv.DictReader(f)}
    with open('dataset/sample_requests.csv', encoding='utf-8') as f:
        samples = {r['request_id']: r for r in csv.DictReader(f)}
    with open('dataset/financial_events.csv', encoding='utf-8') as f:
        events = [e for e in csv.DictReader(f) if e['user_id'] == uid]
    
    p = profiles[uid]
    s = samples[req_id]
    print(f"\n=================== {uid} {req_id} ===================")
    print(f"Req amt: {s['requested_amount']}, Safe today: {s['amount_safe_to_pay']}")
    print(f"Diff needed: {float(s['requested_amount']) - float(s['amount_safe_to_pay'])}")
    print(f"Spending changes: {s['spending_changes_needed']}")
    print(f"Init bal: {p['current_available_balance']}, Min bal: {p['minimum_balance_to_keep']}")
    print(f"Reduce willing: {p['expense_categories_user_is_willing_to_reduce']}")
    print(f"Stop willing: {p['expense_categories_user_is_willing_to_stop']}")

for uid, req_id in [('user_06', 'request_06'), ('user_11', 'request_11'), ('user_21', 'request_21')]:
    inspect_user(uid, req_id)
