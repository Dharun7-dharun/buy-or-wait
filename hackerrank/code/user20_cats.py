import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_20']

from collections import defaultdict
cat_events = defaultdict(list)
for e in events:
    cat_events[e['category']].append(e)

for cat, evs in cat_events.items():
    print(f"Cat {cat}: count={len(evs)}")
    for e in evs[-3:]:
        print(f"   {e['event_id']} {e['direction']} {e['amount']} date={e['event_date']} settle={e['settlement_date']} status={e['status']} desc={e['description']}")
