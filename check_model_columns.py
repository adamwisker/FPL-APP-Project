import joblib

# Load the trained model
model = joblib.load('models/trained_model.pkl')

# Print the feature names the model was trained on
print("Feature names used during model training:")
print(model.feature_names_in_)
