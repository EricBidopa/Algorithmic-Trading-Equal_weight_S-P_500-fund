import pandas
import json

# I am using IEX cloud API
import numpy
import math
import requests
import xlsxwriter

stocks = pandas.read_csv(
    "Algorithmic-Trading-Equal_weight_S-P_500-fund/sp_500_stocks.csv"
)
from Secrets import IEX_CLOUD_API_TOKEN

# i need market cap of each stock and the price(quote) of each stock from the IEX cloud
symbol = "AAPL"
api_url = f"https://cloud.iexapis.com/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}"
# print(api_url)
data = requests.get(api_url).json()
# print(data.status_code) Status code is 403 which on the website means that sandbox is working fine :)
# print(data)

# Getting the price now.
price = data["latestPrice"]
# print(price)
marketcap = data["marketCap"]
# print(marketcap)
# Adding Stock DATA to a pandas dataframe below

myColumns = [
    "Ticker",
    "Stock Price",
    "Market Capitalization",
    "Number of Shares to Buy",
]

finalDataFrame = pandas.DataFrame(columns=myColumns)

# Create a new DataFrame from the Series data
seriesData = pandas.Series([symbol, price, marketcap, "N/A"], index=myColumns)
seriesDataFrame = pandas.DataFrame([seriesData], columns=myColumns)

# Concatenate your finalDataFrame with the seriesDataFrame
finalDataFrame = pandas.concat([finalDataFrame, seriesDataFrame], ignore_index=True)

print(finalDataFrame)


# #.append is deprecated so I had to rewrite to use .concat as shown above
# finalDataFrame = pandas.DataFrame(columns=myColumns)
# # print(finalDataFrame)

# finalDataFrame = finalDataFrame.append(
#     pandas.Series([symbol, price, marketcap, "N/A"], index=myColumns), ignore_index=True
# )
# print(finalDataFrame)


data_frames = []  # Create an empty list to store dataframes
for x in stocks["Ticker"][:100]:
    blockurl = (
        f"https://cloud.iexapis.com/stable/stock/{x}/quote/?token={IEX_CLOUD_API_TOKEN}"
    )
    blockdata = requests.get(blockurl).json()
    # Create a temporary dataframe for each iteration
    temp_df = pandas.DataFrame(
        [[x, blockdata["latestPrice"], blockdata["marketCap"], "N/A"]],
        columns=myColumns,
    )
    data_frames.append(
        temp_df
    )  # Append each temporary dataframe to the list of dataframes

# Concatenate all dataframes in the list
finalDataFrame = pandas.concat(data_frames, ignore_index=True)
# print(finalDataFrame)


# seems append is deprecated so I had to write the code below again using pandas.concat instead as shown  just above.
# # Now I am looping through the stocks csv file to get the price and market cap of each ticker.
# finalDataFrame = pandas.DataFrame(columns=myColumns)
# for x in stocks["Ticker"][
#     :10
# ]:  # going to be really slow because of HTTP request. prolly the slowest in python
#     # print(x) Single API request
#     api_url = (
#         f"https://cloud.iexapis.com/stable/stock/{x}/quote/?token={IEX_CLOUD_API_TOKEN}"
#     )
#     data = requests.get(api_url).json()
#     finalDataFrame = finalDataFrame.append(
#         pandas.Series(
#             [x, data["latestPrice"], data["marketCap"], "N/A"], index=myColumns
#         ),
#         ignore_index=True,
#     )
# # print(finalDataFrame)


portfolioSize = input("Please Enter The Value OF Your Porfolio:  ")
try:
    val = float(portfolioSize)
except ValueError:
    print("Input is not a number")
    portfolioSize = input("Please Enter The Value OF Your Porfolio again:  ")

positionSize = val / len(finalDataFrame.index)
for i in range(0, len(finalDataFrame.index)):
    finalDataFrame.loc[i, "Number of Shares to Buy"] = math.floor(
        positionSize / finalDataFrame.loc[i, "Stock Price"]
    )
print(finalDataFrame)

writer = pandas.ExcelWriter("RecommendedTrades.xlsx", engine="xlsxwriter")
finalDataFrame.to_excel(writer, "RecommendedTrades", index=False)

# Formating Below:

backgroundColor = "#0a0a23"
fontColor = "#00ff00"

string_format = writer.book.add_format(
    {"font_color": fontColor, "bg_color": backgroundColor, "border": 1}
)
dollar_format = writer.book.add_format(
    {
        "num_format": "$0.00",
        "font_color": fontColor,
        "bg_color": backgroundColor,
        "border": 1,
    }
)
integer_format = writer.book.add_format(
    {
        "num_format": "0",
        "font_color": fontColor,
        "bg_color": backgroundColor,
        "border": 1,
    }
)


columnFormats = {
    "A": ["Ticker", string_format],
    "B": ["Stock Price", dollar_format],
    "C": ["Market Capitalization", dollar_format],
    "D": ["Number of Shares to Buy", integer_format],
}
for column in columnFormats.keys():
    writer.sheets["RecommendedTrades"].set_column(
        f"{column}:{column}", 20, columnFormats[column][1]
    )
writer.save()
print(finalDataFrame)

# print(column)
