import pandas as pd

# Step 1: Load the messy file
# This reads the original spreadsheet (CSV) into memory
df = pd.read_csv('data/sms_members_clinical_version.csv')

# Step 2: Drop columns that aren't useful for scoring
# 'notes' and 'system_flag' are just metadata or analyst comments
df = df.drop(columns=['notes', 'system_flag'])

# Step 3; Replace string errors like 'unknown' or 'two with proper missing vaules
df.replace({'unknown': pd.NA, 'two': pd.NA}, inplace=True)

# Step 4: Convert columns to numeric type
# if strings are still in numeric columns, convertthen and turn bad data into NaN
cols_to_convert = ['last_hra_days', 'response_history', 'chronic_conditions', 'age']
for col in cols_to_convert:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Step 5: Drop rows that are missing any of the key fields
# If we can't score them, they shouldn't be ranked
df = df.dropna(subset=cols_to_convert)

# Step 6: Remove duplicate member rows if any 
df = df.drop_duplicates()

# Step 7: Save the cleaned file 
df.to_csv('data/sms_members_cleaned.csv', index=False)
          
print("Complete cleaned members", len(df))