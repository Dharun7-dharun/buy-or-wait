import csv
from datetime import datetime, timedelta
from collections import defaultdict
import numpy as np

def parse_date(s):
    return datetime.strptime(s, '%Y-%m-%d').date()

with open('dataset/sample_requests.csv', encoding='utf-8') as f:
    samples = list(csv.DictReader(f))

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r for r in csv.DictReader(f)}

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = list(csv.DictReader(f))

# Known image amounts
image_amounts = {
    'event_253': 4365000.0,
    'event_1442': 100000.0,
    'event_1545': 41272.0,
    'event_1700': 2854.0,
    'event_1786': 704.05,
    'event_3051': 1995.0,
    'event_3231': 8528.0,
    'event_4535': 15339.0,
    'event_5170': 723.0,
    'event_6033': 79679.26,
    'event_6859': 3650.0,
    'event_7307': 33.50,
    'event_7941': 2298.0,
    'event_9421': 4543.0,
    'event_9806': 9968.0,
    'event_10521': 393.22,
}

# Known salary amendments from messages:
# user_02: 42750000 starting 2025-08-15
# user_06: 1037.52
# user_11: 38760000 (confirmed base)
salary_amendments = {
    'user_02': 42750000.0,
    'user_06': 1037.52,
    'user_11': 38760000.0,
}

print("Loaded base data for fitting.")

def extract_recurring_streams(user_events, req_date):
    # Filter settled events before or on req_date
    past_events = []
    for e in user_events:
        d_str = e['settlement_date'] or e['event_date']
        if not d_str:
            continue
        d = parse_date(d_str)
        if d <= req_date and e['status'] == 'settled':
            past_events.append((d, e))
            
    # Group by (category, description, direction) or category
    by_cat = defaultdict(list)
    for d, e in past_events:
        amt = image_amounts.get(e['event_id'])
        if amt is None and e['amount'].strip():
            amt = float(e['amount'])
        if amt is not None:
            by_cat[e['category']].append((d, amt, e))
            
    streams = []
    for cat, items in by_cat.items():
        if len(items) < 2:
            continue
        items.sort(key=lambda x: x[0])
        dates = [x[0] for x in items]
        intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        amts = [x[1] for x in items]
        direction = items[0][2]['direction']
        
        # Check if monthly (intervals in [28, 31])
        if all(28 <= inv <= 31 for inv in intervals[-3:]):
            dom = dates[-1].day
            streams.append({
                'category': cat,
                'type': 'monthly',
                'day_of_month': dom,
                'last_date': dates[-1],
                'amts': amts,
                'direction': direction,
                'flexibility': items[-1][2]['flexibility'],
                'min_allowed': float(items[-1][2]['minimum_allowed_amount']) if items[-1][2]['minimum_allowed_amount'].strip() else None,
                'event_id': items[-1][2]['event_id'],
            })
        else:
            # Fixed interval in days
            # find most common recent interval
            from collections import Counter
            c = Counter(intervals[-4:])
            mode_inv = c.most_common(1)[0][0]
            streams.append({
                'category': cat,
                'type': 'interval',
                'interval_days': mode_inv,
                'last_date': dates[-1],
                'amts': amts,
                'direction': direction,
                'flexibility': items[-1][2]['flexibility'],
                'min_allowed': float(items[-1][2]['minimum_allowed_amount']) if items[-1][2]['minimum_allowed_amount'].strip() else None,
                'event_id': items[-1][2]['event_id'],
            })
    return streams

for s in samples[:2]:
    uid = s['user_id']
    req_date = parse_date(s['request_date'])
    u_evs = [e for e in events if e['user_id'] == uid]
    st = extract_recurring_streams(u_evs, req_date)
    print(f"\nUser {uid} ({s['request_id']}) streams count={len(st)}:")
    for x in st:
        print(f"  {x['category']:<18} type={x['type']} dom/inv={x.get('day_of_month') or x.get('interval_days')} last={x['last_date']} mean={np.mean(x['amts']):.2f} last_amt={x['amts'][-1]} max={np.max(x['amts']):.2f}")

