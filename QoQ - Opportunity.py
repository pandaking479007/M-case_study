import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Opportunities - Sheet1.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract quarter and year from the 'Date' column
df['Quarter'] = df['Date'].dt.quarter
df['Year'] = df['Date'].dt.year

# Convert 'Amount' to numeric, forcing any non-numeric values to NaN (if they exist)
df['Amount'] = pd.to_numeric(df['Amount'])

# Filter data for Q2 and Q3 of a specific year, e.g., 2024
data_q2 = df[(df['Quarter'] == 2) & (df['Year'] == 2024)]
data_q3 = df[(df['Quarter'] == 3) & (df['Year'] == 2024)]

# Calculate the sum of 'Amount' for each quarter
Amount_q2 = data_q2['Amount'].sum()
Amount_q3 = data_q3['Amount'].sum()

# Create a DataFrame to hold the amounts for each quarter
amounts_df = pd.DataFrame({
    'Quarter': ['Q2', 'Q3'],
    'Amount': [Amount_q2, Amount_q3]
})

# Calculate delta for Q3 vs Q2
amounts_df['Delta_Q3_vs_Q2'] = amounts_df['Amount'].diff().fillna(0)

# Prepare the data for the delta plot
delta_df = amounts_df[['Quarter', 'Delta_Q3_vs_Q2']].set_index('Quarter')

# Use seaborn's 'darkgrid' style to mimic ggplot
sns.set(style="darkgrid")

# Plot the data
fig, ax = plt.subplots(figsize=(12, 6))

# Bar plot for delta changes
delta_df.plot(kind='bar', ax=ax, color=['red'])

# Add annotations on each bar
for p in ax.patches:
    ax.annotate(format(p.get_height(), '.2f'),
                (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center',
                xytext=(0, 10), textcoords='offset points')

# Set titles and labels
ax.set_title('Delta in Total Amount by Quarter (Q2 to Q3)')
ax.set_xlabel('Quarter')
ax.set_ylabel('Delta in Total Amount')

plt.tight_layout()
plt.show()

# Print detailed delta information
print("Delta in Total Amount by Quarter (Q2 to Q3):")
print(amounts_df[['Quarter', 'Delta_Q3_vs_Q2']])
