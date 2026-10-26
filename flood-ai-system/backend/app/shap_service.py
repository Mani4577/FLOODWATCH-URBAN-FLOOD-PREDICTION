from .config import FEATURE_COLUMNS

def format_shap_explanation(shap_values_row):
    contributions = dict(zip(FEATURE_COLUMNS, shap_values_row))

    # Sort by highest impact
    sorted_entries = sorted(
        contributions.items(),
        key=lambda x: abs(x[1]),
        reverse=True
    )[:4]

    total = sum(abs(v) for v in contributions.values()) or 1.0

    return [
        {
            "feature": f,
            "importance_pct": float(round(abs(v) / total * 100, 2)),
            "impact": float(round(v, 5))
        }
        for f, v in sorted_entries
    ]