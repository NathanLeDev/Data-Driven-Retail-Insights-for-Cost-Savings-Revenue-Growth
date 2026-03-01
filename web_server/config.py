"""
Configuration constants for the Retail Analytics Streamlit App
"""

# Cluster/Persona definitions
CLUSTER_NAMES = {
    0: "The Premium Healths",
    1: "The Daily Economizers",
    2: "The Budget-Healthy Mix"
}

CLUSTER_COLORS = {
    0: "#1f77b4",  # Blue
    1: "#ff7f0e",  # Orange
    2: "#2ca02c"   # Green
}

# Cluster profiles (from clustering notebook results)
CLUSTER_PROFILES = {
    0: {
        "name": "The Premium Healths",
        "size_pct": 24.91,
        "order_frequency": 4.66,
        "reorder_ratio": 0.654,
        "avg_basket_size": 11.77,
        "HAI": 0.876,
        "PSI": 0.499,
        "description": "High frequency, high loyalty, health-conscious shoppers"
    },
    1: {
        "name": "The Daily Economizers",
        "size_pct": 36.66,
        "order_frequency": 0.80,
        "reorder_ratio": 0.404,
        "avg_basket_size": 5.12,
        "HAI": 0.863,
        "PSI": 0.493,
        "description": "Low frequency, smaller baskets, price-sensitive"
    },
    2: {
        "name": "The Budget-Healthy Mix",
        "size_pct": 38.43,
        "order_frequency": 0.58,
        "reorder_ratio": 0.346,
        "avg_basket_size": 13.46,
        "HAI": 0.867,
        "PSI": 0.497,
        "description": "Large baskets, weekend shoppers, balanced health focus"
    }
}

# Features used for clustering
FEATURES_LIST = [
    'order_frequency',
    'reorder_ratio',
    'avg_basket_size',
    'avg_basket_value',
    'weekend_basket_intensity',
    'driver_dependency',
    'niche_affinity_score',
    'aisle_penetration',
    'HAI',
    'PSI'
]

# Validated association rules (from notebook 03_association_rules)
ASSOCIATION_RULES = [
    {"antecedent": "Large Lemon", "consequent": "Banana", "confidence": 0.268, "lift": 1.78, "support": 0.012},
    {"antecedent": "Organic Raspberries", "consequent": "Organic Strawberries", "confidence": 0.249, "lift": 2.96, "support": 0.011},
    {"antecedent": "Organic Strawberries", "consequent": "Bag of Organic Bananas", "confidence": 0.234, "lift": 1.94, "support": 0.018},
    {"antecedent": "Organic Strawberries", "consequent": "Banana", "confidence": 0.212, "lift": 1.41, "support": 0.016},
    {"antecedent": "Strawberries", "consequent": "Banana", "confidence": 0.290, "lift": 1.93, "support": 0.014},
    {"antecedent": "Limes", "consequent": "Banana", "confidence": 0.225, "lift": 1.50, "support": 0.010},
    {"antecedent": "Organic Baby Spinach", "consequent": "Banana", "confidence": 0.213, "lift": 1.42, "support": 0.019},
    {"antecedent": "Organic Baby Spinach", "consequent": "Bag of Organic Bananas", "confidence": 0.210, "lift": 1.74, "support": 0.018},
    {"antecedent": "Organic Avocado", "consequent": "Banana", "confidence": 0.303, "lift": 2.02, "support": 0.015},
    {"antecedent": "Organic Hass Avocado", "consequent": "Bag of Organic Bananas", "confidence": 0.295, "lift": 2.45, "support": 0.021},
    {"antecedent": "Organic Fuji Apple", "consequent": "Banana", "confidence": 0.278, "lift": 1.85, "support": 0.011},
    {"antecedent": "Organic Yellow Onion", "consequent": "Banana", "confidence": 0.241, "lift": 1.61, "support": 0.010},
    {"antecedent": "Organic Garlic", "consequent": "Banana", "confidence": 0.232, "lift": 1.55, "support": 0.010},
    {"antecedent": "Honeycrisp Apple", "consequent": "Banana", "confidence": 0.267, "lift": 1.78, "support": 0.012},
]

# Day labels for temporal analysis
DAY_LABELS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

# Data paths
DATA_PATH = "data/processed/df_full.parquet"
REPORTS_PATH = "reports"

# App configuration
APP_TITLE = "Retail Analytics Dashboard"
APP_ICON = ""

# =============================================================================
# BOSS MODE - Executive View Configuration
# =============================================================================

# Simple customer segment names for Boss (values from 05_pipeline_clustering.ipynb)
BOSS_SEGMENTS = {
    0: {
        "name": "Premium Customers",
        "share": "25%",
        "value": "65% loyalty, 11.8 items/basket",
        "action": "Retain with VIP program and premium organic products"
    },
    1: {
        "name": "Budget Shoppers",
        "share": "37%",
        "value": "14 items/basket, highest volume",
        "action": "Target with promotions and value bundles"
    },
    2: {
        "name": "Weekend Families",
        "share": "38%",
        "value": "Smaller baskets, price sensitive",
        "action": "Weekend promotions and family products"
    }
}

# Key business insights for Boss (all values from notebooks)
BOSS_KEY_INSIGHTS = {
    "revenue_potential": "5,378€",
    "revenue_description": "Net profit from validated promotions",
    "savings_potential": "174€",
    "savings_description": "Losses avoided (blocked unprofitable promos)",
    "best_time": "Sunday 10am-2pm",
    "best_time_description": "Peak ordering window (+44% vs weekdays)"
}

# Top bundle recommendations for Boss (simple language)
BOSS_BUNDLES = [
    {"bundle": "Organic Avocado + Organic Bananas", "gain": "+145%", "why": "Bought together 3x more often"},
    {"bundle": "Organic Strawberries + Organic Raspberries", "gain": "+196%", "why": "Very popular berry combo"},
    {"bundle": "Organic Spinach + Bananas", "gain": "+74%", "why": "Popular health combo"},
    {"bundle": "Lemons + Bananas", "gain": "+78%", "why": "Frequent association"},
    {"bundle": "Strawberries + Bananas", "gain": "+93%", "why": "Breakfast classic"},
]

# Executive summary points (all values from notebooks)
BOSS_SUMMARY = [
    "**5,378€ net profit** from validated promotional campaigns",
    "**50,649 personalized offers** generated by prediction engine",
    "**174€ losses avoided** by blocking unprofitable promotions",
    "**Sunday** = +44% more orders than weekday average",
    "**59% average reorder rate** - loyal customer base to leverage"
]

# ROI Analysis data (from 08_business_impact_ROI.ipynb)
ROI_DATA = {
    "approved_profit": 5378.44,
    "avoided_losses": 173.62,
    "total_offers": 50649,
    "total_rules": 224,
    "margin_rates": {
        "alcohol": 0.40,
        "personal_care": 0.35,
        "household": 0.30,
        "produce": 0.35,
        "meat_seafood": 0.25,
        "pantry": 0.25,
        "snacks": 0.25,
        "beverages": 0.25,
        "dairy_eggs": 0.15,
        "babies": 0.15,
        "frozen": 0.25
    },
    "uplift_model": {
        0.10: 1.15,  # 10% discount -> +15% purchase probability
        0.20: 1.35   # 20% discount -> +35% purchase probability
    },
    "cannibalization_factor": 0.70
}

# Golden Basket configuration (from 06_golden-basket-per-cluster.ipynb)
GOLDEN_BASKET_WEIGHTS = {
    0: {"name": "Premium Healths", "health": 0.7, "price": 0.1, "popularity": 0.2},
    1: {"name": "Daily Economizers", "health": 0.1, "price": 0.7, "popularity": 0.2},
    2: {"name": "Budget-Healthy Mix", "health": 0.4, "price": 0.4, "popularity": 0.2}
}

PRODUCT_ROLES = ["core", "companion", "niche", "opportunistic", "filler"]
