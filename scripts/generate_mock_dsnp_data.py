import pandas as pd
import numpy as np

np.random.seed(42)
n_members = 14000

member_id = [f"M{str(i).zfill(5)}" for i in range(1, n_members + 1)]
hra_overdue_days = np.random.exponential(scale=120, size=n_members).astype(int)
hra_overdue_days = np.clip(hra_overdue_days, 0, 365)

response_history = np.random.choice([0, 1, 2, 3, 4, 5], size=n_members, p=[0.35, 0.25, 0.15, 0.10, 0.10, 0.05])
chronic_conditions = np.random.poisson(lam=2.2, size=n_members)
chronic_conditions = np.clip(chronic_conditions, 0, 6)

age = np.random.normal(loc=74, scale=5, size=n_members).astype(int)
age = np.clip(age, 65, 90)

prior_hra_completed = np.random.binomial(1, 0.65, n_members)
managed_flag = np.random.binomial(1, 0.15, n_members)
high_risk_flag = np.random.binomial(1, 0.13, n_members)
recent_kickout_flag = np.random.binomial(1, 0.08, n_members)

# Generate risk-correlated ER visits
# Base rate varies by risk factors: age, chronic conditions, high_risk_flag
base_er_rate = 0.3
er_lambda = (
    base_er_rate +
    (age >= 75).astype(float) * 0.25 +  # Older members have more ER visits
    (chronic_conditions >= 4).astype(float) * 0.35 +  # Multiple chronic conditions increase ER use
    high_risk_flag.astype(float) * 0.4 +  # High-risk members have elevated ER utilization
    (managed_flag == 0).astype(float) * 0.15  # Unmanaged members have slightly higher ER use
)
er_visit_count = np.array([np.random.poisson(lam=lam) for lam in er_lambda])
er_visit_count = np.clip(er_visit_count, 0, 5)

dsnp_flag = np.ones(n_members, dtype=int)

region_code = np.random.choice([1, 2, 3, 4], size=n_members, p=[0.2, 0.25, 0.35, 0.2])
social_vulnerability_score = np.round(np.random.beta(a=2, b=5, size=n_members), 2)
text_opt_in = np.random.binomial(1, 0.82, n_members)

df_mock = pd.DataFrame({
    "member_id": member_id,
    "hra_overdue_days": hra_overdue_days,
    "response_history": response_history,
    "chronic_conditions": chronic_conditions,
    "age": age,
    "prior_hra_completed": prior_hra_completed,
    "managed_flag": managed_flag,
    "high_risk_flag": high_risk_flag,
    "recent_kickout_flag": recent_kickout_flag,
    "er_visit_count": er_visit_count,
    "dsnp_flag": dsnp_flag,
    "region_code": region_code,
    "social_vulnerability_score": social_vulnerability_score,
    "text_opt_in": text_opt_in
})

df_mock.to_csv("mock_dsnp_members.csv", index=False)
