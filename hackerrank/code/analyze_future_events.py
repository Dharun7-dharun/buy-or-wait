import csv
from datetime import datetime, timedelta

def analyze_user(uid, req_id):
    with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
        profiles = {r['user_id']: r for r in csv.DictReader(f)}
    with open('dataset/sample_requests.csv', encoding='utf-8') as f:
        samples = {r['request_id']: r for r in csv.DictReader(f)}
    with open('dataset/financial_events.csv', encoding='utf-8') as f:
        events = [e for e in csv.DictReader(f) if e['user_id'] == uid]
    with open('dataset/messages.csv', encoding='utf-8') as f:
        messages = [m for m in csv.DictReader(f) if m['user_id'] == uid]

    p = profiles[uid]
    s = samples[req_id]
    req_date = datetime.strptime(s['request_date'], '%Y-%m-%d').date()
    end_date = req_date + timedelta(days=90)

    print(f"==================================================")
    print(f"User: {uid} | Request: {req_id} ({s['request_date']} to {end_date})")
    print(f"Home Curr: {p['home_currency']} | Init Bal: {p['current_available_balance']} | Min Bal: {p['minimum_balance_to_keep']}")
    print(f"Req Amount: {s['requested_amount']} | Safe Today: {s['amount_safe_to_pay']} | Earliest Full: {s['earliest_date_for_full_payment']}")
    print(f"Status: {s['affordability_status']} | Method: {s['recommended_payment_method']}")
    print(f"Prot cats: {p['expense_categories_to_protect']}")
    print(f"Reduce cats: {p['expense_categories_user_is_willing_to_reduce']}")
    print(f"Stop cats: {p['expense_categories_user_is_willing_to_stop']}")
    
    print("\n--- Events with date/settle >= req_date ---")
    for e in events:
        d_str = e['settlement_date'] or e['event_date']
        d = datetime.strptime(d_str, '%Y-%m-%d').date()
        if d >= req_date:
            print(f"  {e['event_id']} | {e['event_type']} | {e['category']} | {e['direction']} | amt={e['amount']} | date={e['event_date']} | settle={e['settlement_date']} | status={e['status']} | flex={e['flexibility']} | desc={e['description']}")

    print("\n--- Messages ---")
    for m in messages:
        print(f"  {m['message_id']} | sent={m['sent_at']} | src={m['source_type']} | text={m['message_text']}")

for uid, req_id in [('user_01', 'request_01'), ('user_02', 'request_02'), ('user_03', 'request_03'), ('user_04', 'request_04'), ('user_05', 'request_05')]:
    analyze_user(uid, req_id)
