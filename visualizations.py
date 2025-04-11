import pandas as pd
import requests
import matplotlib.pyplot as plt
import boto3
from botocore.exceptions import NoCredentialsError

# Define your FMP API Key
FMP_API_KEY = ''

# List of bank tickers
tickers = ['JPM', 'BAC', 'C', 'WFC', 'GS']

# Construct the API request URL
HTTP_request = f'https://financialmodelingprep.com/api/v3/historical-price-full/{",".join(tickers)}?apikey={FMP_API_KEY}'

# Fetch data using requests and parse the JSON response
response = requests.get(HTTP_request)
data = response.json()

# Extract the 'historicalStockList' key from the data
historical_stock_list = data.get('historicalStockList', [])

# Create a DataFrame for storing stock prices
series_list = []
for stock in historical_stock_list:
    historical_data = pd.DataFrame(stock['historical'])
    series_list.append(historical_data['close'])  # Extract 'close' prices

# Extract dates from the first ticker
dates = pd.DataFrame(historical_stock_list[0]['historical'])['date']
series_list.append(dates)  # Add dates to the series list

# Set up column names
column_names = tickers + ['Date']

# Combine all series into a single DataFrame
bank_data = pd.concat(series_list, axis=1)
bank_data.columns = column_names
bank_data.set_index('Date', inplace=True)

# Print the resulting DataFrame
print(bank_data)

########################
# Create a figure with subplots
########################
plt.figure(figsize=(18, 12))

########################
# Subplot 1: Boxplot of Bank Stock Prices
########################
plt.subplot(2, 2, 1)

# Generate the boxplot
plt.boxplot(bank_data.values, tick_labels=bank_data.columns)

# Add titles to the chart and axes
plt.title('Boxplot of Bank Stock Prices (5Y Lookback)', fontsize=16)
plt.xlabel('Bank', fontsize=14)
plt.ylabel('Stock Prices', fontsize=14)

########################
# Subplot 2: Wells Fargo Stock Prices (Scatterplot)
########################
plt.subplot(2, 2, 2)

# Prepare data
dates = [pd.to_datetime(d) for d in bank_data.index]
WFC_stock_prices = bank_data['WFC']

# Generate the scatterplot
plt.scatter(dates, WFC_stock_prices, alpha=0.7)

# Add titles to the chart and axes
plt.title("Wells Fargo Stock Price (5Y Lookback)", fontsize=16)
plt.ylabel("Stock Price", fontsize=14)
plt.xlabel("Date", fontsize=14)

########################
# Subplot 3: Bank of America Stock Prices (Scatterplot)
########################
plt.subplot(2, 2, 3)

# Prepare data
BAC_stock_prices = bank_data['BAC']

# Generate the scatterplot
plt.scatter(dates, BAC_stock_prices, alpha=0.7, color='green')

# Add titles to the chart and axes
plt.title("Bank of America Stock Price (5Y Lookback)", fontsize=16)
plt.ylabel("Stock Price", fontsize=14)
plt.xlabel("Date", fontsize=14)

########################
# Subplot 4: Histogram of Daily Closing Stock Prices
########################
plt.subplot(2, 2, 4)

# Generate the histogram
plt.hist(bank_data.transpose(), bins=30, alpha=0.7)

# Add a legend to the histogram
plt.legend(bank_data.columns, fontsize=12)

# Add titles to the chart and axes
plt.title("Histogram of Daily Closing Stock Prices for the 5 Largest Banks (5Y Lookback)", fontsize=16)
plt.ylabel("Observations", fontsize=14)
plt.xlabel("Stock Prices", fontsize=14)

########################
# Adjust layout and save the plots locally
########################
plt.tight_layout()
visualization_file = 'bank_data_plots.png'
plt.savefig(visualization_file)
plt.show()
print(f"Visualization saved locally as {visualization_file}")

################################################
# Push the saved file to the AWS S3 bucket
################################################
bucket_name = 'saideepthibucket'
s3_file_name = visualization_file

try:
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(
        visualization_file,  # Local file name
        bucket_name,  # S3 bucket name
        s3_file_name,  # File name in S3 bucket
        ExtraArgs={'ACL': 'public-read'}  # Make publicly accessible
    )
    print(f"Visualization uploaded to S3 as {s3_file_name}")
except NoCredentialsError:
    print("No AWS credentials found. Make sure your credentials are configured correctly.")
except Exception as e:
    print(f"An error occurred while uploading: {e}")
