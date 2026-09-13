import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_04']

print(f"User 04 events: {len(events)}")
for e in events:
    print(f"{e['event_id']} | {e['category']} | {e['direction']} | amt={e['amount']} | date={e['event_date']} | settle={e['settlement_date']} | status={e['status']} | flex={e['flexibility']} | desc={e['description']}")
