import pandas as pd

if __name__ == '__main__':
    # Step 1: Load the cleaned data set
    df = pd.read_csv('data/sms_members_cleaned.csv')

    # Step 2: Risk scoring logic
    df['score'] = (
        (1 / (df['last_hra_days'] + 1)) * 80 +
        (df['response_history'] * 15) + 
        (df['chronic_conditions'] * 20) + 
        (df['age'] > 75).astype(int) * 10 + 
        (df['dual_eligible'] * 10) +
        (df['snp_member'] * 15) 
    )

    # Step 3: Assign risk tiers (Low, Medium, High)
    df['risk_tier'] = pd.qcut(df['score'], q=3, labels=['Low', 'Medium', 'High'])
    df.to_csv('data/sms_outreach_ranked.csv', index=False)

    # Step 4: Flag DSNP HRA-overdue members for mock SMS campaign
    df['eligible_for_sms'] = (
        (df['snp_member'] == 1) &
        (df['dual_eligible'] == 1) &
        (df['last_hra_days'] > 100) &
        (df['response_history'] <= 2) & 
        (df['age'] >= 65) &
        (df['chronic_conditions'] >= 2)
    )

    # Step 5: Sort by score
    df = df.sort_values(by='score', ascending=False)

    # Step 6: Save the ranked and segmented output 
    df.to_csv('data/sms_outreach_ranked.csv', index=False)

    # Step 7: Output summary stats
    eligible = df[df['eligible_for_sms'] == True]
    tier_based_eligible = df[df['risk_tier'].isin(['High', 'Medium'])]
    
    print("\nTotal members by risk tier (entire dataset):")
    print(df['risk_tier'].value_counts())
    
    print("\nStrictly eligible members:", len(eligible))
    print(eligible['risk_tier']).value_counts()

    print("\nTier-based eligible members:", len(tier_based_eligible))
    print(tier_based_eligible['risk_tier'].value_counts())

    print("\nScoring summary for strictly eligible members:")
    print("Average score:", round(eligible['score'].mean(), 2))

    print("\n Scoring complete. Summary of SMS pilot-eligible segment:")
    print("Total eligible members", len(eligible))
    print("Average score:", round(eligible['score'].mean(), 2))
    print("Risk tier breakdown:")
    print(eligible['risk_tier'].value_counts())

    # Step 8: Group profile summary
    group_summary = eligible.groupby('risk_tier')[['age', 'chronic_conditions', 'last_hra_days']].mean().round(1)
    print("\nGroup profile by risk tier:")
    print(group_summary)
    print("\nData saved to: data/sms_outreach_ranked.csv")