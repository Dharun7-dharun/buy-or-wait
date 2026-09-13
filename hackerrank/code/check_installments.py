import csv

with open('dataset/sample_requests.csv', encoding='utf-8') as f:
    samples = list(csv.DictReader(f))

with open('dataset/financial_profiles.csv', encoding='utf-8') as f:
    profiles = {r['user_id']: r for r in csv.DictReader(f)}

with open('dataset/request_payment_options.csv', encoding='utf-8') as f:
    options = list(csv.DictReader(f))

for s in samples:
    if s['recommended_payment_method'] == 'installments':
        req_id = s['request_id']
        uid = s['user_id']
        p = profiles[uid]
        opts = [o for o in options if o['request_id'] == req_id]
        print(f"\nRequest: {req_id} | User: {uid} | Max inst months: {p['max_installment_months']}")
        print(f"  Chosen Plan: {s['payment_plan']}")
        print(f"  Available options:")
        for o in opts:
            print(f"    {o['payment_option_id']} | method={o['payment_method']} | n_payments={o['number_of_payments']} | amt={o['payment_amount']} | freq={o['payment_frequency_days']} | first={o['first_payment_date']} | total={o['total_payable_amount']}")
