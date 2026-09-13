import csv

# User 02 events:
with open('dataset/financial_events.csv', encoding='utf-8') as f:
    u2_events = [e for e in csv.DictReader(f) if e['user_id'] == 'user_02']

# Known amounts for user 02:
# event_185: 1651100
# insurance: 1132400
# education: 3040000
# cloud_storage: 369550
# Sum of fixed knowns:
fixed_sum = 1651100 + 1132400 + 3040000 + 369550
print(f"Fixed sum = {fixed_sum}")
print(f"Target sum = 13996350")
rem = 13996350 - fixed_sum
print(f"Remaining for (utilities, healthcare, transport, groceries) = {rem}")

# Check past amounts for utilities, healthcare, transport, groceries:
for cat in ['utilities', 'healthcare', 'transport', 'groceries']:
    evs = [e for e in u2_events if e['category'] == cat and e['status'] == 'settled']
    amts = [float(e['amount']) for e in evs]
    print(f"{cat}: count={len(amts)}, mean={sum(amts)/len(amts):.2f}, last={amts[-1]}, max={max(amts)}")
