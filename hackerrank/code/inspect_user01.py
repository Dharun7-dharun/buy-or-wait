import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_01']

print(f"Total events for user_01: {len(events)}")
categories = set(e['category'] for e in events)
print("Categories:", categories)

for cat in sorted(categories):
    cat_events = [e for e in events if e['category'] == cat]
    print(f"\n--- Category: {cat} (count={len(cat_events)}) ---")
    for e in cat_events:
        print(f"  {e['event_id']:<10} {e['direction']:<7} amt={e['amount']:<10} date={e['event_date']} settle={e['settlement_date']} status={e['status']:<10} flex={e['flexibility']:<12} desc={e['description']}")
