import csv
import json
from collections import Counter

def inspect_enums():
    def get_column_values(filepath, cols):
        with open(filepath, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            res = {col: set() for col in cols}
            for row in reader:
                for col in cols:
                    val = row[col].strip()
                    if val:
                        res[col].add(val)
        return res

    print("--- ENUMS IN DATASET ---")
    fp_enums = get_column_values("dataset/financial_profiles.csv", [
        'home_currency', 'payment_methods_user_will_consider'
    ])
    print("financial_profiles currencies:", fp_enums['home_currency'])
    print("financial_profiles payment methods sets:", fp_enums['payment_methods_user_will_consider'])

    fe_enums = get_column_values("dataset/financial_events.csv", [
        'event_type', 'category', 'direction', 'status', 'flexibility'
    ])
    for k, v in fe_enums.items():
        print(f"financial_events {k}:", sorted(list(v)))

    rpo_enums = get_column_values("dataset/request_payment_options.csv", [
        'payment_method'
    ])
    print("request_payment_options payment_method:", sorted(list(rpo_enums['payment_method'])))

    req_enums = get_column_values("dataset/requests.csv", [
        'request_type', 'allows_partial_payment'
    ])
    for k, v in req_enums.items():
        print(f"requests {k}:", sorted(list(v)))

    sample_enums = get_column_values("dataset/sample_requests.csv", [
        'affordability_status', 'recommended_payment_method'
    ])
    for k, v in sample_enums.items():
        print(f"sample_requests {k}:", sorted(list(v)))

if __name__ == '__main__':
    inspect_enums()
