import sys
sys.path.append(".")
from src.data_loader import load_data

df = load_data("data/insurance_data.csv")

# Drop duplicates and rows where both TotalPremium and TotalClaims are null
df = df.drop_duplicates()
df = df.dropna(subset=["TotalPremium", "TotalClaims"])

df.to_csv("data/insurance_data_cleaned.csv", index=False)
print(f"Cleaned data saved: {len(df)} rows")
