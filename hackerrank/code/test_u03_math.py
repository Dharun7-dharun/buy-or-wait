import csv

# We want to see what expenses before Sept 15 sum to 2,268,600
# Rent: 1,140,000
# Pending: 95,000
# Remaining to account for: 2,268,600 - 1,140,000 - 95,000 = 1,033,600

print(f"Target sum of expenses: 2268600")
print(f"Rent + Pending = 1140000 + 95000 = {1140000 + 95000}")
print(f"Remaining = {2268600 - 1140000 - 95000}")
