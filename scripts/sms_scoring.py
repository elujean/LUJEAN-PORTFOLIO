import pandas as pd
import numpy as np

df = pd.read_csv("data/mock_dsnp_members.csv")

df = df[df['managed_flag'] == 0]

def log_scale(days, max_days=365):
    """Log-normalize HRA overdue days to a 0–1 scale"""
    return np.log1p(days) / np.log1p(max_days)

df['outreach_score'] = (
    log_scale(df['hra_overdue_days']) * 30 +
    (1 - df['response_history'] / 5) * 15 +
    (df['chronic_conditions'] * 4) +
    (df['age'] >= 75).astype(int) * 8 +
    (df['prior_hra_completed']) * 5 +
    (df['high_risk_flag']) * 20 +
    (df['recent_kickout_flag']) * -10 +
    (df['er_visit_count'] > 1).astype(int) * 10
)

def assign_tier(score):
    if score >= 80:
        return 'High'
    elif score >= 55:
        return 'Medium'
    else:
        return 'Low'


df['outreach_priority'] = df['outreach_score'].apply(assign_tier)
np.random.seed(42)
optin_probs = {
    'High': 0.70,
    'Medium': 0.80,
    'Low': 0.90
}
df['text_opt_in'] = df['outreach_priority'].apply(
    lambda tier: np.random.binomial(1, optin_probs[tier])
)

df.to_csv("data/sms_outreach_ranked.csv", index=False)


print(df[['member_id', 'outreach_score', 'outreach_priority']].head(10))
