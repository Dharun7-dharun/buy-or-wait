import csv

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r['home_currency'] for r in csv.DictReader(f)}

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = list(csv.DictReader(f))

fx_events = [e for e in events if e['currency'] != profiles[e['user_id']]]
print(f"Total events with foreign currency: {len(fx_events)}")

# Check foreign currency samples
for e in fx_events[:10]:
    uid = e['user_id']
    home_curr = profiles[uid]
    print(f"User {uid} (Home: {home_curr}) | Event {e['event_id']} | Date: {e['event_date']} | Settle: {e['settlement_date']} | Curr: {e['currency']} | Amt: {e['amount']} | Status: {e['status']}")
