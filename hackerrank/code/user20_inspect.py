import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_20']

with open('dataset/messages.csv', encoding='utf-8') as f:
    messages = [m for m in csv.DictReader(f) if m['user_id'] == 'user_20']

print(f"User 20 events: {len(events)}")
for e in events[-25:]:
    print(f"{e['event_id']} | {e['category']} | {e['direction']} | amt={e['amount']} | date={e['event_date']} | settle={e['settlement_date']} | status={e['status']} | flex={e['flexibility']} | desc={e['description']}")

print("\nMessages:")
for m in messages:
    print(m)
