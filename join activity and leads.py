import pandas as pd

# File paths
file_path_activities = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Activities - Sheet1.csv'
file_path_leads = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Leads - Sheet1.csv'
output_file_path = r'C:\Users\lanji\OneDrive\Desktop\merged_table.csv'

# Columns to exclude for each file
columns_to_exclude_activities = [ 'ActivityDate', 'Status', 'AssignedEmployeeId', 'Time of Day', 'DateKey', 'Date']
columns_to_exclude_leads = ['Title', 'Industry', 'Employees', 'CreatedDate', 'OwnerEmployeeId', 'TimeZone', 'Date Key']

# Read the CSV files into DataFrames, specifying dtypes or setting low_memory=False
df_activities = pd.read_csv(file_path_activities, low_memory=False)
df_leads = pd.read_csv(file_path_leads, low_memory=False)

# Drop specified columns
df_activities_cleaned = df_activities.drop(columns=columns_to_exclude_activities)
df_leads_cleaned = df_leads.drop(columns=columns_to_exclude_leads)

# Merge the DataFrames on 'LeadId' column
merged_table = pd.merge(df_activities_cleaned, df_leads_cleaned, on='LeadId', how='inner')

# Export the merged table to a CSV file
merged_table.to_csv(output_file_path, index=False)

# Display the merged table
print(merged_table)

print(f'Merged table successfully saved to {output_file_path}')
