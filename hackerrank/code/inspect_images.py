import csv

with open('dataset/images.csv', encoding='utf-8') as f:
    images = list(csv.DictReader(f))

with open('dataset/financial_events.csv', encoding='utf-8') as f:
    events = {e['event_id']: e for e in csv.DictReader(f)}

print(f"Total images: {len(images)}")
for img in images:
    ev = events.get(img['related_event_id'], {})
    print(f"Image {img['image_id']} | User {img['user_id']} | Req {img['request_id']} | Event {img['related_event_id']}")
    print(f"  Event type: {ev.get('event_type')} | Cat: {ev.get('category')} | Curr: {ev.get('currency')} | Date: {ev.get('event_date')} | Desc: {ev.get('description')}")
