import pandas as pd
from sklearn.ensemble import IsolationForest
import pickle

# Load
train = pd.read_csv("C:\Users\Dnyandip\OneDrive\Desktop\ThreatIntelligence\data\Train_clean_dataset.csv")

# Model
model = IsolationForest(n_estimators=200, contamination=0.1, random_state=42)
model.fit(train)

# Save
with open("model/model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ Model trained & saved!")