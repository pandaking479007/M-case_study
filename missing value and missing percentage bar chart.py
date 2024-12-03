import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Updated Activities - Sheet1.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Display the first few rows of the DataFrame
print(df.head())

# Check for missing values
missing_values = df.isnull().sum()
missing_percentage = (missing_values / len(df)) * 100

# Create a DataFrame for plotting
missing_data = pd.DataFrame({
    'Total Missing Values': missing_values,
    'Percentage Missing': missing_percentage
})

# Plotting the bar chart
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plotting the percentage of missing values
bars1 = missing_data['Percentage Missing'].plot(kind='bar', color='skyblue', ax=ax1, position=1, width=0.4)
ax1.set_ylabel('Percentage', color='skyblue')
ax1.set_xlabel('Columns')
ax1.set_title('Missing Values Analysis')
ax1.tick_params(axis='y', labelcolor='skyblue')

# Adding percentage labels
for p in bars1.containers:
    bars1.bar_label(p, label_type='edge', fmt='%.2f%%')

# Creating a secondary y-axis to plot the total missing values
ax2 = ax1.twinx()
bars2 = missing_data['Total Missing Values'].plot(kind='bar', color='orange', ax=ax2, position=2.4, width=0.4)
ax2.set_ylabel('Total Missing Values', color='orange')
ax2.tick_params(axis='y', labelcolor='orange')

# Adding total missing values labels
for p in bars2.containers:
    bars2.bar_label(p, label_type='edge')

# Adjust the layout to make space for the x-axis labels
plt.subplots_adjust(left=0.2, bottom=0.22, right=0.8, top=0.9)

plt.show()

