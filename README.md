# Algorithmic-Trading-Equal_weight_S-P_500-fund
 Equal weight S&P 500 fund


# Algorithmic Trading with Equal-Weight S&P 500 Fund
This project is a Python implementation of a trading algorithm that utilizes
 equal-weight allocation to the S&P 500 fund. The script uses the IEX Cloud API to obtain 
 the market cap and price of each stock in the S&P 500, and then calculates the number of 
 shares to buy for a given portfolio value.

# Dependencies
pandas
numpy
requests
xlsxwriter

# Getting Started
Clone the repository
Install the dependencies
Create an account on IEX Cloud and obtain an API token
Create a Secrets.py file in the project directory and assign your 
API token to IEX_CLOUD_API_TOKEN variable in the file.
Run the trading.py script.

# How it works
Read the sp_500_stocks.csv file to obtain the list of stocks in the S&P 500.
Use the IEX Cloud API to obtain the market cap and price of each stock in the S&P 500.
Calculate the number of shares to buy for a given portfolio value and equal-weight 
allocation to each stock.
Create an Excel file (RecommendedTrades.xlsx) with the recommended trades.
Format the Excel file with custom colors and fonts.

# Usage
Run the main.py script.
Enter the value of your portfolio when prompted.
Wait for the script to complete.
Check the RecommendedTrades.xlsx file for the recommended trades.
Note: The API usage is limited to sandbox mode only. To use the actual API, 
a paid subscription is required.


# Cheers! ++EAJ++
