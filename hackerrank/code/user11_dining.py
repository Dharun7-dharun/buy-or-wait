import csv

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_11' and e['category'] == 'dining']

print("User 11 dining events:")
for e in events:
    print(e['event_id'], e['amount'], e['settlement_date'], e['status'], e['flexibility'], e['minimum_allowed_amount'], e['description'])
