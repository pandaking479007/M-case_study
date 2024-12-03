import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.arima.model import ARIMA

# Replace 'path_to_your_file.csv' with the actual path to your CSV file
file_path = r'C:\Users\lanji\OneDrive\Desktop\Cleaned - Updated Opportunities - Sheet1.csv'

# List of columns to exclude
columns_to_exclude = ['CreatedDate', 'DemoCreated', 'AcceptedDecisionDate', 'OwnerEmployeeId', 'OwnerEmployee', 'DateKey', 'AcceptedDateKey', 'Accepted_date', 'Converted from chat']

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Drop the specified columns
df = df.drop(columns=columns_to_exclude)

# Filter rows where 'Opp Converted' is 1
df = df[df['Opp Converted'] == 1]

# Convert 'Date' to datetime format
df['Date'] = pd.to_datetime(df['Date'])

# Extract quarter and year from the 'Date' column
df['Quarter'] = df['Date'].dt.quarter
df['Year'] = df['Date'].dt.year

# Filter data for Q1, Q2, and Q3 of a specific year, e.g., 2024
data_q1 = df[(df['Quarter'] == 1) & (df['Year'] == 2024)]
data_q2 = df[(df['Quarter'] == 2) & (df['Year'] == 2024)]
data_q3 = df[(df['Quarter'] == 3) & (df['Year'] == 2024)]

# Calculate the sum of 'Amount' for each quarter
Amount_q1 = data_q1['Amount'].sum()
Amount_q2 = data_q2['Amount'].sum()
Amount_q3 = data_q3['Amount'].sum()

# Prepare the data for linear regression
quarters = np.array([1, 2, 3]).reshape(-1, 1)  # Quarters Q1, Q2, Q3
amounts = np.array([Amount_q1, Amount_q2, Amount_q3])  # Corresponding amounts

# Create and fit the linear regression model
lin_model = LinearRegression()
lin_model.fit(quarters, amounts)

# Predict the amount for Q4 using linear regression
Q4_lin_prediction = lin_model.predict(np.array([4]).reshape(-1, 1))[0]

# Prepare the data as a time series for ARIMA
quarters_labels = pd.period_range(start='2024Q1', periods=3, freq='Q')
time_series = pd.Series(amounts, index=quarters_labels)

# Fit the ARIMA model
arima_model = ARIMA(time_series, order=(1, 1, 1))
arima_model_fit = arima_model.fit()

# Forecast the next quarter (Q4) using ARIMA
Q4_arima_forecast = arima_model_fit.forecast(steps=1)
Q4_arima_prediction = Q4_arima_forecast[0]

# Prepare data for plotting
quarters_labels = quarters_labels.append(pd.PeriodIndex(['2024Q4'], freq='Q'))
amounts_lin = np.append(amounts, Q4_lin_prediction)
amounts_arima = np.append(amounts, Q4_arima_prediction)

# Plot the historical data and forecasts with ggplot2 style
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

# Historical data
plt.plot(quarters_labels[:-1].to_timestamp(), amounts, 'o-', label='Historical Data')

# Linear Regression Forecast
plt.plot([quarters_labels[2].to_timestamp(), quarters_labels[3].to_timestamp()], [amounts[2], amounts_lin[3]], 'r--', label='Linear Regression Q4 Forecast')
plt.plot(quarters_labels[3].to_timestamp(), amounts_lin[3], 'ro')

# ARIMA Forecast
plt.plot([quarters_labels[2].to_timestamp(), quarters_labels[3].to_timestamp()], [amounts[2], amounts_arima[3]], 'b--', label='ARIMA Q4 Forecast')
plt.plot(quarters_labels[3].to_timestamp(), amounts_arima[3], 'bo')

# Add annotations for each point in "$xxxK" format, rounded up
for i, txt in enumerate(amounts):
    plt.annotate(f'${np.ceil(txt / 1000):.0f}K', (quarters_labels[i].to_timestamp(), txt), textcoords="offset points", xytext=(0, 10), ha='center')
plt.annotate(f'${np.ceil(Q4_lin_prediction / 1000):.0f}K', (quarters_labels[-1].to_timestamp(), Q4_lin_prediction), textcoords="offset points", xytext=(0, 10), ha='center', color='red')
plt.annotate(f'${np.ceil(Q4_arima_prediction / 1000):.0f}K', (quarters_labels[-1].to_timestamp(), Q4_arima_prediction), textcoords="offset points", xytext=(0, 10), ha='center', color='blue')

# Update y-axis to "$xxx,000" format
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,}K".format(int(x / 1000))))

plt.xlabel('Quarter')
plt.ylabel('Amount ($)')
plt.title('Sum Amount by Quarter and Forecast for Q4 (Converted Opportunities)')
plt.xticks(ticks=quarters_labels.to_timestamp(), labels=[str(period) for period in quarters_labels])
plt.legend()
plt.grid(True)
# Adjust the layout to make space for the x-axis labels
plt.subplots_adjust(left=0.2, bottom=0.22, right=0.8, top=0.9)
plt.show()

# Display the forecasted amounts for Q4
print(f'Forecasted Amount for Q4 using Linear Regression: ${Q4_lin_prediction:.2f}')
print(f'Forecasted Amount for Q4 using ARIMA: ${Q4_arima_prediction:.2f}')
