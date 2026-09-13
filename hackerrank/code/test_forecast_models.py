import csv
from datetime import datetime, timedelta
from collections import defaultdict

def parse_date(d_str):
    return datetime.strptime(d_str, '%Y-%m-%d').date()

def format_date(d):
    return d.strftime('%Y-%m-%d')

# Let's inspect the exact target values for all 25 samples
with open('dataset/sample_requests.csv', encoding='utf-8') as f:
    samples = list(csv.DictReader(f))

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r for r in csv.DictReader(f)}

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    all_events = list(csv.DictReader(f))

with open('dataset/messages.csv', encoding='utf-8') as f:
    all_messages = list(csv.DictReader(f))

# Let's print for each sample:
# user_id, req_date, requested_amount, current_bal, min_bal, amount_safe_to_pay, earliest_date
print("Sample ground truth summary:")
for s in samples:
    p = profiles[s['user_id']]
    print(f"{s['request_id']} ({s['user_id']}) req={s['request_date']} amt={s['requested_amount']} cur={p['current_available_balance']} min={p['minimum_balance_to_keep']} safe={s['amount_safe_to_pay']} ear={s['earliest_date_for_full_payment']} status={s['affordability_status']}")
