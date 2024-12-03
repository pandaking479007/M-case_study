import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Function to format numbers compactly
def format_number(num):
    if num >= 1_000_000:
        return f'{num/1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num/1_000:.1f}K'
    else:
        return str(num)

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Updated Leads - Sheet1.csv'

columns_to_exclude = ['Industry_cleaned' ,'OwnerEmployee','Date']



# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)
# Drop the specified columns
df = df.drop(columns=columns_to_exclude)

# Display the first few rows of the DataFrame
print(df.head())

# Check for missing values
missing_values = df.isnull().sum()

# Print the number of missing values in each column
print("Missing values in each column:\n", missing_values)


