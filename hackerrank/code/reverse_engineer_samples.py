import csv
from datetime import datetime, timedelta
from collections import defaultdict

def load_data():
    with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
        profiles = {r['user_id']: r for r in csv.DictReader(f)}
    with open('dataset/sample_requests.csv', encoding='utf-8') as f:
        samples = list(csv.DictReader(f))
    with open('dataset/financial_events.csv', encoding='utf-8') as f:
        events = list(csv.DictReader(f))
    with open('dataset/messages.csv', encoding='utf-8') as f:
        messages = list(csv.DictReader(f))
    with open('dataset/request_payment_options.csv', encoding='utf-8') as f:
        options = list(csv.DictReader(f))
    with open('dataset/images.csv', encoding='utf-8') as f:
        images = list(csv.DictReader(f))
    with open('dataset/exchange_rates.csv', encoding='utf-8') as f:
        rates = list(csv.DictReader(f))
    return profiles, samples, events, messages, options, images, rates

profiles, samples, events, messages, options, images, rates = load_data()

# Group events by user
user_events = defaultdict(list)
for e in events:
    user_events[e['user_id']].append(e)

print(f"Loaded {len(profiles)} profiles, {len(samples)} samples, {len(events)} events, {len(messages)} messages.")

# Let's inspect the recurring patterns across the dataset
# For each sample, let's look at user's events grouped by category and description
for s in samples[:5]:
    uid = s['user_id']
    req_date = datetime.strptime(s['request_date'], '%Y-%m-%d').date()
    print(f"\n==================== Sample {s['request_id']} User {uid} ====================")
    print(f"Req Date: {req_date}, Req Amt: {s['requested_amount']}, Safe Today: {s['amount_safe_to_pay']}")
    print(f"Status: {s['affordability_status']}, Method: {s['recommended_payment_method']}")
    print(f"Plan: {s['payment_plan']}")
    print(f"Changes: {s['spending_changes_needed']}")
    
    # Analyze categories
    cat_events = defaultdict(list)
    for e in user_events[uid]:
        cat_events[e['category']].append(e)
        
    for cat, evs in cat_events.items():
        # sort by date
        evs.sort(key=lambda x: x['settlement_date'] or x['event_date'])
        dates = [datetime.strptime(x['settlement_date'] or x['event_date'], '%Y-%m-%d').date() for x in evs]
        intervals = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        amts = [float(x['amount']) if x['amount'].strip() else None for x in evs]
        status_set = set(x['status'] for x in evs)
        flex_set = set(x['flexibility'] for x in evs)
        print(f"  Category: {cat:<18} count={len(evs):<3} intervals={intervals[-4:]} amts={amts[-3:]} flex={flex_set} status={status_set}")
