import csv
from datetime import date, timedelta
from collections import defaultdict, Counter

with open('dataset/sample_requests.csv', encoding='utf-8') as f:
    samples = list(csv.DictReader(f))

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r for r in csv.DictReader(f)}

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = list(csv.DictReader(f))

# Let's inspect each sample request:
# What was the salary for that user?
for s in samples:
    uid = s['user_id']
    req_date = date.fromisoformat(s['request_date'])
    u_events = [e for e in events if e['user_id'] == uid]
    sal_events = [e for e in u_events if e['category'] == 'salary']
    print(f"\n{s['request_id']} ({uid}) req_date={req_date} safe_target={s['amount_safe_to_pay']} status_target={s['affordability_status']}")
    for se in sal_events:
        print(f"   Salary: id={se['event_id']} amt={se['amount']} status={se['status']} date={se['event_date']} settle={se['settlement_date']} desc={se['description']}")
