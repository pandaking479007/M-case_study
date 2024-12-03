import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Activities - Sheet1.csv'

# List of columns to exclude
columns_to_exclude = ['ActivityId', 'ActivityDate', 'Status','AssignedEmployeeId','AssignedEmployee','LeadId','Time of Day','DateKey','Date']

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Drop the specified columns
df = df.drop(columns=columns_to_exclude)

# Convert categorical columns to numerical values using one-hot encoding
df_encoded = pd.get_dummies(df)

# Generate the correlation matrix for one-hot encoded data
corr_matrix = df_encoded.corr()

# Create a mask for correlations with absolute values less than 0.5
mask_numbers = np.abs(corr_matrix) < 0.5

# Set up the matplotlib figure with a larger size if necessary
plt.figure(figsize=(24, 20))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap without the masked annotations
heatmap = sns.heatmap(corr_matrix, cmap=cmap, vmax=1.0, center=0,
                      square=True, linewidths=0.5, cbar_kws={"shrink": 0.75},
                      xticklabels=True, yticklabels=True, annot=False)  # Remove all annotations

# Add annotations for values >= 0.5
for i in range(len(corr_matrix.columns)):
    for j in range(len(corr_matrix.columns)):
        if np.abs(corr_matrix.iloc[i, j]) >= 0:
            heatmap.text(j + 0.5, i + 0.5, f'{corr_matrix.iloc[i, j]:.2f}',
                         ha='center', va='center', color='black', fontsize=10)

# Adjust the layout to make space for the x-axis labels
plt.subplots_adjust(left=0.2, bottom=0.22, right=0.8, top=0.9)

# Set axis titles
heatmap.set_xlabel('Feature', fontsize=16)
heatmap.set_ylabel('Feature', fontsize=16)

# Set the title of the heatmap
plt.title('Activity Correlation Analysis', fontsize=20)
plt.xticks(rotation=90, fontsize=12)  # Rotate x-axis labels for better readability
plt.yticks(rotation=0, fontsize=12)  # Keep y-axis labels horizontal with larger font size

plt.show()
