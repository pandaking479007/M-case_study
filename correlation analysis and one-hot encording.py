import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import chi2_contingency

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Activities - Sheet1.csv'

# List of columns to exclude
columns_to_exclude = ['ActivityId', 'ActivityDate', 'Status','AssignedEmployeeId','LeadId','Time of Day','DateKey','Date']  # Replace with your column names

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Drop the specified columns
df = df.drop(columns=columns_to_exclude)

# Convert categorical columns to numerical values using one-hot encoding
df_encoded = pd.get_dummies(df)

# Generate the correlation matrix for one-hot encoded data
corr_matrix = df_encoded.corr()

# Create a mask for the upper triangle
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))

# Set up the matplotlib figure
plt.figure(figsize=(20, 20))

# Generate a custom diverging colormap
cmap = sns.diverging_palette(230, 20, as_cmap=True)

# Draw the heatmap with the mask and correct aspect ratio
heatmap=sns.heatmap(corr_matrix, mask=mask, cmap=cmap, vmax=1.0, center=0, square=True,
                    linewidths=0.5, cbar_kws={"shrink": 0.75}, annot=True, fmt='.2f')

# Adjust the layout to make space for the x-axis labels
plt.subplots_adjust(bottom=0.25)
# Set axis titles
heatmap.set_xlabel('Feature')
heatmap.set_ylabel('Feature')
plt.title('One-Hot encording correlation analysis')
plt.show()
