import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Updated Opportunities - Sheet1.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Replace 'Outcome' with the actual name of the column you want to analyze
column_name = ('Date')

# Count the unique string values in the specified column
value_counts = df[column_name].value_counts()

# Print the counts of each unique value
print(f"Counts of each unique value in the '{column_name}' column:\n", value_counts)

# Plot the counts of each unique value as a bar chart
plt.figure(figsize=(13,10 ))
bars=value_counts.plot(kind='bar', color='#15192b')
for bar in bars.containers:
    bars.bar_label(bar, label_type='edge')
plt.title(f'Counts of Each Unique Value in the \'{column_name}\' Column')
plt.xlabel('Unique Values')
plt.ylabel('Counts')
plt.xticks(rotation=20)
plt.show()
