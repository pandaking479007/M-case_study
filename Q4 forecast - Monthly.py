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

# Extract month and year from the 'Date' column
df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Filter data for months 1 to 9 of a specific year, e.g., 2024
data_jan = df[(df['Month'] == 1) & (df['Year'] == 2024)]
data_feb = df[(df['Month'] == 2) & (df['Year'] == 2024)]
data_mar = df[(df['Month'] == 3) & (df['Year'] == 2024)]
data_apr = df[(df['Month'] == 4) & (df['Year'] == 2024)]
data_may = df[(df['Month'] == 5) & (df['Year'] == 2024)]
data_jun = df[(df['Month'] == 6) & (df['Year'] == 2024)]
data_jul = df[(df['Month'] == 7) & (df['Year'] == 2024)]
data_aug = df[(df['Month'] == 8) & (df['Year'] == 2024)]
data_sep = df[(df['Month'] == 9) & (df['Year'] == 2024)]

# Calculate the sum of 'Amount' for each month
Amount_jan = data_jan['Amount'].sum()
Amount_feb = data_feb['Amount'].sum()
Amount_mar = data_mar['Amount'].sum()
Amount_apr = data_apr['Amount'].sum()
Amount_may = data_may['Amount'].sum()
Amount_jun = data_jun['Amount'].sum()
Amount_jul = data_jul['Amount'].sum()
Amount_aug = data_aug['Amount'].sum()
Amount_sep = data_sep['Amount'].sum()

# Prepare the data for linear regression
months = np.array(range(1, 10)).reshape(-1, 1)  # Months 1 to 9
amounts = np.array([Amount_jan, Amount_feb, Amount_mar, Amount_apr, Amount_may, Amount_jun, Amount_jul, Amount_aug, Amount_sep])  # Corresponding amounts

# Create and fit the linear regression model
lin_model = LinearRegression()
lin_model.fit(months, amounts)

# Predict the amounts for Oct, Nov, and Dec using linear regression
months_forecast = np.array([10, 11, 12]).reshape(-1, 1)
lin_forecast = lin_model.predict(months_forecast)

# Prepare the data as a time series for ARIMA
months_labels = pd.date_range(start='2024-01', periods=9, freq='M')
time_series = pd.Series(amounts, index=months_labels)

# Fit the ARIMA model
arima_model = ARIMA(time_series, order=(1, 1, 1))
arima_model_fit = arima_model.fit()

# Forecast the next three months (Oct, Nov, Dec) using ARIMA
arima_forecast = arima_model_fit.forecast(steps=3)
arima_predictions = arima_forecast.values

# Prepare data for plotting
months_labels = months_labels.append(pd.date_range(start='2024-10', periods=3, freq='M'))
amounts_lin = np.append(amounts, lin_forecast)
amounts_arima = np.append(amounts, arima_predictions)

# Plot the historical data and forecasts with ggplot2 style
plt.style.use('ggplot')
plt.figure(figsize=(10, 6))

# Historical data
plt.plot(months_labels[:9], amounts, 'o-', label='Historical Data')

# Linear Regression Forecast
plt.plot(months_labels[8:], amounts_lin[8:], 'r--', label='Linear Regression Forecast')
plt.plot(months_labels[9:], lin_forecast, 'ro')

# ARIMA Forecast
plt.plot(months_labels[8:], amounts_arima[8:], 'b--', label='ARIMA Forecast')
plt.plot(months_labels[9:], arima_predictions, 'bo')

# Add annotations for each point in "$xxxK" format, rounded up
for i, txt in enumerate(amounts):
    plt.annotate(f'${np.ceil(txt / 1000):.0f}K', (months_labels[i], txt), textcoords="offset points", xytext=(0, 10), ha='center')
for i in range(3):
    plt.annotate(f'${np.ceil(lin_forecast[i] / 1000):.0f}K', (months_labels[9+i], lin_forecast[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='red')
    plt.annotate(f'${np.ceil(arima_predictions[i] / 1000):.0f}K', (months_labels[9+i], arima_predictions[i]), textcoords="offset points", xytext=(0, 10), ha='center', color='blue')

# Update y-axis to "$xxx,000" format
plt.gca().get_yaxis().set_major_formatter(plt.FuncFormatter(lambda x, loc: "${:,}K".format(int(x / 1000))))

# Rotate the x-axis labels by 90 degrees
plt.xticks(ticks=months_labels, labels=[date.strftime('%b %Y') for date in months_labels], rotation=90)

plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.title('Sum Amount by Month and Forecast for Oct-Dec (Converted Opportunities)')
plt.legend()
plt.grid(True)
# Adjust the layout to make space for the x-axis labels
plt.subplots_adjust(left=0.2, bottom=0.22, right=0.8, top=0.9)
plt.show()

# Display the forecasted amounts for Oct-Dec
for i, month in enumerate(['October', 'November', 'December']):
    print(f'Forecasted Amount for {month} using Linear Regression: ${lin_forecast[i]:.2f}')
    print(f'Forecasted Amount for {month} using ARIMA: ${arima_predictions[i]:.2f}')
