import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_05']

print(f"User 05 events count: {len(events)}")
# Let's inspect events from 2025-10-01 to 2025-11-06
for e in events:
    d = e['settlement_date'] or e['event_date']
    if d >= '2025-10-01':
        print(f"  {e['event_id']} | {e['category']} | {e['direction']} | amt={e['amount']} | date={e['event_date']} | settle={e['settlement_date']} | status={e['status']} | flex={e['flexibility']} | desc={e['description']}")
