import csv
from collections import Counter

with open('dataset/messages.csv', encoding='utf-8') as f:
    msgs = list(csv.DictReader(f))

print(f"Total messages: {len(msgs)}")
src_types = Counter(m['source_type'] for m in msgs)
print("Source types:", src_types)

# Sample messages per source type
for st in src_types:
    st_msgs = [m for m in msgs if m['source_type'] == st]
    print(f"\n--- Source Type: {st} (count={len(st_msgs)}) ---")
    for m in st_msgs[:3]:
        print(f"  ID: {m['message_id']} | User: {m['user_id']} | Req: {m['request_id']} | RelEvent: {m['related_event_id']}")
        print(f"    Text: {m['message_text']}")
