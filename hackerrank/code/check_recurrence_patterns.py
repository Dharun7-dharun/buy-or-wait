import csv
from collections import defaultdict

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = list(csv.DictReader(f))

user_cats = defaultdict(lambda: defaultdict(list))
for e in events:
    user_cats[e['user_id']][e['category']].append(e)

print(f"Total users with events: {len(user_cats)}")
# Check all distinct categories
all_cats = sorted(list(set(e['category'] for e in events)))
print("All categories in events:", all_cats)

# For each category, see how many users have it, and what are typical intervals
cat_user_counts = defaultdict(int)
cat_intervals = defaultdict(list)

for uid, cats in user_cats.items():
    for cat, evs in cats.items():
        cat_user_counts[cat] += 1
        if len(evs) >= 2:
            evs_sorted = sorted(evs, key=lambda x: x['settlement_date'] or x['event_date'])
            # check days between
            from datetime import datetime
            dates = [datetime.strptime(x['settlement_date'] or x['event_date'], '%Y-%m-%d').date() for x in evs_sorted]
            diffs = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
            cat_intervals[cat].extend(diffs)

for cat in all_cats:
    ivals = cat_intervals[cat]
    print(f"Cat: {cat:<20} users={cat_user_counts[cat]:<3} total_events={sum(len(user_cats[u][cat]) for u in user_cats):<5}")
    if ivals:
        # print common intervals
        from collections import Counter
        top_diffs = Counter(ivals).most_common(5)
        print(f"    intervals: {top_diffs}")
