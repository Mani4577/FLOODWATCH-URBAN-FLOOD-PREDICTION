import joblib
import os
from .config import MODEL_PATH

_model = None

def get_model():
    global _model
    if _model is None:
        if not os.path.exists(MODEL_PATH):
            alt1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "models", "rainfall_flood_model.pkl"))
            alt2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "models", "rainfall_flood_model.pkl"))
            if os.path.exists(alt1):
                model_file = alt1
            elif os.path.exists(alt2):
                model_file = alt2
            else:
                raise FileNotFoundError(f"Model not found in {MODEL_PATH} or {alt1} or {alt2}")
        else:
            model_file = MODEL_PATH

        _model = joblib.load(model_file)
    return _model
