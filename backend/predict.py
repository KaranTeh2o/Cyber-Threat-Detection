import pickle

# Load model
model = pickle.load(open("model/model.pkl", "rb"))

def predict(data):
    result = model.predict([data])
    return "Threat" if result[0] == -1 else "Normal"